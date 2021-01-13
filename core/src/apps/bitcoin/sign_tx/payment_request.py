from storage import cache
from trezor import wire
from trezor.crypto.curve import secp256k1
from trezor.crypto.hashlib import sha256
from trezor.enums import MemoType
from trezor.utils import HashWriter

from apps.common import coininfo
from apps.common.address_mac import check_address_mac
from apps.common.keychain import Keychain

from .. import writers

if False:
    from trezor.messages import TxOutput
    from trezor.messages import TxAckPaymentRequest
    from apps.common.coininfo import CoinInfo


class PaymentRequestVerifier:
    if __debug__:
        # secp256k1 public key of m/0h for "all all ... all" seed.
        PUBLIC_KEY = b"\x03\x0f\xdf^(\x9bZ\xefSb\x90\x95:\xe8\x1c\xe6\x0e\x84\x1f\xf9V\xf3f\xac\x12?\xa6\x9d\xb3\xc7\x9f!\xb0"
    else:
        PUBLIC_KEY = b""

    def __init__(
        self, msg: TxAckPaymentRequest, coin: CoinInfo, keychain: Keychain
    ) -> None:
        self.h_outputs = HashWriter(sha256())
        self.amount = 0
        self.expected_amount = msg.amount
        self.signature = msg.signature
        self.h_pr = HashWriter(sha256())

        if msg.nonce:
            nonce = bytes(msg.nonce)
            if cache.get(cache.APP_COMMON_NONCE) != nonce:
                raise wire.DataError("Invalid nonce in payment request.")
            cache.delete(cache.APP_COMMON_NONCE)
        else:
            nonce = b""
            if msg.memos:
                wire.DataError("Missing nonce in payment request.")

        writers.write_bytes_fixed(self.h_pr, b"SL\x00\x24", 4)
        writers.write_bytes_prefixed(self.h_pr, nonce)
        writers.write_bytes_prefixed(self.h_pr, msg.recipient_name.encode())
        writers.write_bitcoin_varint(self.h_pr, len(msg.memos))
        for memo in msg.memos:
            writers.write_uint32(self.h_pr, memo.type)
            if memo.type == MemoType.COIN_PURCHASE:
                assert memo.amount is not None  # checked by sanitizer
                assert memo.coin_name is not None  # checked by sanitizer
                assert memo.mac is not None  # checked by sanitizer
                memo_coin = coininfo.by_name(memo.coin_name)
                check_address_mac(memo.data, memo.mac, memo_coin, keychain)
                writers.write_uint32(self.h_pr, memo_coin.slip44)
                writers.write_uint64(self.h_pr, memo.amount)

            writers.write_bytes_prefixed(self.h_pr, memo.data)

        writers.write_uint32(self.h_pr, coin.slip44)

    def verify(self) -> None:
        if self.expected_amount is not None and self.amount != self.expected_amount:
            raise wire.DataError("Invalid amount in payment request.")

        hash_outputs = writers.get_tx_hash(self.h_outputs)
        writers.write_bytes_fixed(self.h_pr, hash_outputs, 32)

        if not secp256k1.verify(
            self.PUBLIC_KEY, self.signature, self.h_pr.get_digest()
        ):
            raise wire.DataError("Invalid signature in payment request.")

    def _add_output(self, txo: TxOutput) -> None:
        # For change outputs txo.address filled in by output_derive_script().
        assert txo.address is not None
        writers.write_uint64(self.h_outputs, txo.amount)
        writers.write_bytes_prefixed(self.h_outputs, txo.address.encode())

    def add_external_output(self, txo: TxOutput) -> None:
        self._add_output(txo)
        self.amount += txo.amount

    def add_change_output(self, txo: TxOutput) -> None:
        self._add_output(txo)