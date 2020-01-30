""" Globally unique and URL-suitable object identifier """

import uuid
import hashlib
import base58

def guauoid_generate():

    # Create a node- and time-based UUID (version 1), 128 Bits.
    plain_uuid = uuid.uuid1()

    # Hash this UUID using the variable length hash SHAKE-128 XOF
    # to produce an 8 byte binary hash (64 bits).
    hashed_uuid = hashlib.shake_128(plain_uuid.bytes).digest(8)

    # Encode using Base58 including checksum. This will result in
    # a typeable identifier with a length of at most 16 characters.
    # The checksum is not necessary since the encoded value carries
    # no meaning to the application. It will however enable validation
    # at any time, e.g. to protect the user against typos.
    encoded_uuid = base58.b58encode_check(hashed_uuid)

    return encoded_uuid.decode('utf-8')
