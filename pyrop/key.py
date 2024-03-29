'''Key proxies
'''
__version__ = "0.14.0"

# Copyright (c) 2020 Janky <box@janky.tech>
# All right reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
# OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.

from weakref import ref as weakref
from datetime import datetime, timedelta
from .rop.lib import ROPD
from .rop.err import ROPE
from .error import RopError
from .util import _get_rop_data, _call_rop_func, _new_rop_obj, _get_str_prop, _ts2datetime, \
        _timedelta2sec


class RopUidHandle(object):
    '''UID proxy
    '''

    def __init__(self, own, huid):
        self.__own = weakref(own)
        self.__lib = own.lib
        if huid is None or huid.value is None:
            raise RopError(self.__own().ROP_ERROR_NULL_HANDLE)
        self.__huid = huid

    def _close(self):
        ret = self.__lib.rnp_uid_handle_destroy(self.__huid)
        self.__huid = None
        return ret

    @property
    def handle(self): return self.__huid

    # API

    def get_type(self):
        return _call_rop_func(self.__lib.rnp_uid_get_type, 1, self.__huid)

    def get_data(self):
        data, dlen = _call_rop_func(self.__lib.rnp_uid_get_data, 2, self.__huid)
        return _get_rop_data(self.__lib, ROPE.RNP_SUCCESS, data, dlen)

    @property
    def is_primary(self):
        return _call_rop_func(self.__lib.rnp_uid_is_primary, 1, self.__huid)
    @property
    def is_valid(self):
        return _call_rop_func(self.__lib.rnp_uid_is_valid, 1, self.__huid)
    @property
    def signature_count(self):
        return _call_rop_func(self.__lib.rnp_uid_get_signature_count, 1, self.__huid)
    @property
    def is_revoked(self):
        return _call_rop_func(self.__lib.rnp_uid_is_revoked, 1, self.__huid)

    def get_signature_at(self, idx, tag=0):
        sign = _call_rop_func(self.__lib.rnp_uid_get_signature_at, 1, self.__huid, idx)
        return _new_rop_obj(self.__own(), ROPE.RNP_SUCCESS, sign, RopSign, tag)

    def get_revocation_signature(self, tag=0):
        sign = _call_rop_func(self.__lib.rnp_uid_get_revocation_signature, 1, self.__huid)
        return _new_rop_obj(self.__own(), ROPE.RNP_SUCCESS, sign, RopSign, tag)


class RopKey(object):
    '''Key proxy
    '''

    def __init__(self, own, kid):
        self.__own = weakref(own)
        self.__lib = own.lib
        if kid is None or kid.value is None:
            raise RopError(self.__own().ROP_ERROR_NULL_HANDLE)
        self.__kid = kid

    def _close(self):
        ret = ROPE.RNP_SUCCESS
        if self.__kid is not None:
            ret = self.__lib.rnp_key_handle_destroy(self.__kid)
            self.__kid = None
        return ret

    def _detach(self):
        self.__kid = None

    @property
    def handle(self): return self.__kid

    # API

    @property
    def keyid(self):
        return _get_str_prop(self.__lib, self.__lib.rnp_key_get_keyid, self.__kid)
    @property
    def alg(self):
        return _get_str_prop(self.__lib, self.__lib.rnp_key_get_alg, self.__kid)
    @property
    def primary_grip(self):
        return _get_str_prop(self.__lib, self.__lib.rnp_key_get_primary_grip, self.__kid)
    @property
    def primary_fprint(self):
        return _get_str_prop(self.__lib, self.__lib.rnp_key_get_primary_fprint, self.__kid)
    @property
    def fprint(self):
        return _get_str_prop(self.__lib, self.__lib.rnp_key_get_fprint, self.__kid)
    @property
    def grip(self):
        return _get_str_prop(self.__lib, self.__lib.rnp_key_get_grip, self.__kid)
    @property
    def primary_uid(self):
        return _get_str_prop(self.__lib, self.__lib.rnp_key_get_primary_uid, self.__kid)
    @property
    def curve(self):
        return _get_str_prop(self.__lib, self.__lib.rnp_key_get_curve, self.__kid)
    @property
    def revocation_reason(self):
        return _get_str_prop(self.__lib, self.__lib.rnp_key_get_revocation_reason, self.__kid)

    def set_expiration(self, expiry):
        _call_rop_func(self.__lib.rnp_key_set_expiration, 0, self.__kid, _timedelta2sec(expiry));

    @property
    def is_valid(self):
        return _call_rop_func(self.__lib.rnp_key_is_valid, 1, self.__kid)
    @property
    def valid_till(self):
        tms = _call_rop_func(self.__lib.rnp_key_valid_till, 1, self.__kid)
        dtime = _ts2datetime(tms)
        if tms == 0:
            dtime = datetime.min;
        elif tms == 0xffffffff:
            dtime = datetime.max;
        return dtime
    @property
    def is_revoked(self):
        return _call_rop_func(self.__lib.rnp_key_is_revoked, 1, self.__kid)
    @property
    def is_superseded(self):
        return _call_rop_func(self.__lib.rnp_key_is_superseded, 1, self.__kid)
    @property
    def is_compromised(self):
        return _call_rop_func(self.__lib.rnp_key_is_compromised, 1, self.__kid)
    @property
    def is_retired(self):
        return _call_rop_func(self.__lib.rnp_key_is_retired, 1, self.__kid)
    @property
    def is_locked(self):
        return _call_rop_func(self.__lib.rnp_key_is_locked, 1, self.__kid)
    @property
    def protection_type(self):
        return _get_str_prop(self.__lib, self.__lib.rnp_key_get_protection_type, self.__kid)
    @property
    def protection_mode(self):
        return _get_str_prop(self.__lib, self.__lib.rnp_key_get_protection_mode, self.__kid)
    @property
    def protection_cipher(self):
        return _get_str_prop(self.__lib, self.__lib.rnp_key_get_protection_cipher, self.__kid)
    @property
    def protection_hash(self):
        return _get_str_prop(self.__lib, self.__lib.rnp_key_get_protection_hash, self.__kid)
    @property
    def protection_iterations(self):
        return _call_rop_func(self.__lib.rnp_key_get_protection_iterations, 1, self.__kid)
    @property
    def is_protected(self):
        return _call_rop_func(self.__lib.rnp_key_is_protected, 1, self.__kid)
    @property
    def is_primary(self):
        return _call_rop_func(self.__lib.rnp_key_is_primary, 1, self.__kid)
    @property
    def is_sub(self):
        return _call_rop_func(self.__lib.rnp_key_is_sub, 1, self.__kid)
    @property
    def have_secret(self):
        return _call_rop_func(self.__lib.rnp_key_have_secret, 1, self.__kid)
    @property
    def have_public(self):
        return _call_rop_func(self.__lib.rnp_key_have_public, 1, self.__kid)
    @property
    def creation(self):
        tms = _call_rop_func(self.__lib.rnp_key_get_creation, 1, self.__kid)
        return _ts2datetime(tms)
    @property
    def expiration(self):
        return timedelta(seconds=_call_rop_func(self.__lib.rnp_key_get_expiration, 1, self.__kid))
    @property
    def uid_count(self):
        return _call_rop_func(self.__lib.rnp_key_get_uid_count, 1, self.__kid)
    @property
    def signature_count(self):
        return _call_rop_func(self.__lib.rnp_key_get_signature_count, 1, self.__kid)
    @property
    def bits(self):
        return _call_rop_func(self.__lib.rnp_key_get_bits, 1, self.__kid)
    @property
    def dsa_qbits(self):
        return _call_rop_func(self.__lib.rnp_key_get_dsa_qbits, 1, self.__kid)
    @property
    def subkey_count(self):
        return _call_rop_func(self.__lib.rnp_key_get_subkey_count, 1, self.__kid)

    def get_uid_at(self, idx):
        return _get_str_prop(self.__lib, self.__lib.rnp_key_get_uid_at, self.__kid, idx)

    def to_json(self, public_mpis=False, secret_mpis=False, signatures=False, sign_mpis=False):
        flags = (ROPD.RNP_JSON_PUBLIC_MPIS if public_mpis else 0)
        flags |= (ROPD.RNP_JSON_SECRET_MPIS if secret_mpis else 0)
        flags |= (ROPD.RNP_JSON_SIGNATURES if signatures else 0)
        flags |= (ROPD.RNP_JSON_SIGNATURE_MPIS if sign_mpis else 0)
        return _get_str_prop(self.__lib, self.__lib.rnp_key_to_json, self.__kid, flags)

    def packets_to_json(self, secret, mpi=False, raw=False, grip=False):
        flags = (ROPD.RNP_JSON_DUMP_MPI if mpi else 0)
        flags |= (ROPD.RNP_JSON_DUMP_RAW if raw else 0)
        flags |= (ROPD.RNP_JSON_DUMP_GRIP if grip else 0)
        return _get_str_prop(self.__lib, self.__lib.rnp_key_packets_to_json, self.__kid, \
            secret, flags)

    def allows_usage(self, usage):
        return _call_rop_func(self.__lib.rnp_key_allows_usage, 1, self.__kid, usage)

    def allows_usages(self, usages):
        for usage in usages:
            if not self.allows_usage(usage):
                return False
        return True

    def disallows_usages(self, usages):
        for usage in usages:
            if self.allows_usage(usage):
                return False
        return True

    def lock(self):
        _call_rop_func(self.__lib.rnp_key_lock, 0, self.__kid)

    def unlock(self, password):
        _call_rop_func(self.__lib.rnp_key_unlock, 0, self.__kid, password)

    def get_uid_handle_at(self, idx, tag=0):
        huid = _call_rop_func(self.__lib.rnp_key_get_uid_handle_at, 1, self.__kid, idx)
        return _new_rop_obj(self.__own(), ROPE.RNP_SUCCESS, huid, RopUidHandle, tag)

    def protect(self, password, cipher, cipher_mode, hash_, iterations):
        _call_rop_func(self.__lib.rnp_key_protect, 0, self.__kid, password, cipher, \
            cipher_mode, hash_, iterations)

    def unprotect(self, password):
        _call_rop_func(self.__lib.rnp_key_unprotect, 0, self.__kid, password)

    def public_key_data(self):
        data, dlen = _call_rop_func(self.__lib.rnp_get_public_key_data, 2, self.__kid)
        return _get_rop_data(self.__lib, ROPE.RNP_SUCCESS, data, dlen)

    def secret_key_data(self):
        data, dlen = _call_rop_func(self.__lib.rnp_get_secret_key_data, 2, self.__kid)
        return _get_rop_data(self.__lib, ROPE.RNP_SUCCESS, data, dlen)

    def add_uid(self, uid, hash_, expiration, key_flags, primary):
        _call_rop_func(self.__lib.rnp_key_add_uid, 0, self.__kid, uid, hash_, expiration, \
            key_flags, primary)

    def get_subkey_at(self, idx, tag=0):
        skey = _call_rop_func(self.__lib.rnp_key_get_subkey_at, 1, self.__kid, idx)
        return _new_rop_obj(self.__own(), ROPE.RNP_SUCCESS, skey, RopKey, tag)

    def get_signature_at(self, idx, tag=0):
        sign = _call_rop_func(self.__lib.rnp_key_get_signature_at, 1, self.__kid, idx)
        return _new_rop_obj(self.__own(), ROPE.RNP_SUCCESS, sign, RopSign, tag)

    def get_revocation_signature(self, tag=0):
        sign = _call_rop_func(self.__lib.rnp_key_get_revocation_signature, 1, self.__kid)
        return _new_rop_obj(self.__own(), ROPE.RNP_SUCCESS, sign, RopSign, tag)

    def export(self, output, public=True, secret=True, subkey=False, armored=False):
        outp = (output.handle if output is not None else None)
        flags = (ROPD.RNP_KEY_EXPORT_PUBLIC if public else 0)
        flags |= (ROPD.RNP_KEY_EXPORT_SECRET if secret else 0)
        flags |= (ROPD.RNP_KEY_EXPORT_SUBKEYS if subkey else 0)
        flags |= (ROPD.RNP_KEY_EXPORT_ARMORED if armored else 0)
        _call_rop_func(self.__lib.rnp_key_export, 0, self.__kid, outp, flags)

    def export_public(self, output, **kwargs):
        self.export(output, public=True, secret=False, **kwargs)

    def export_secret(self, output, **kwargs):
        self.export(output, public=False, secret=True, **kwargs)

    def export_autocrypt(self, subkey, uid, output):
        subk = (subkey.handle if subkey is not None else None)
        outp = (output.handle if output is not None else None)
        _call_rop_func(self.__lib.rnp_key_export_autocrypt, 0, self.__kid, subk, uid, outp, 0)

    def remove(self, public=True, secret=True, subkeys=False):
        flags = (ROPD.RNP_KEY_REMOVE_PUBLIC if public else 0)
        flags |= (ROPD.RNP_KEY_REMOVE_SECRET if secret else 0)
        flags |= (ROPD.RNP_KEY_REMOVE_SUBKEYS if subkeys else 0)
        _call_rop_func(self.__lib.rnp_key_remove, 0, self.__kid, flags)

    def remove_public(self, subkeys=False):
        self.remove(True, False, subkeys)

    def remove_secret(self, subkeys=False):
        self.remove(False, True, subkeys)

    def export_revocation(self, output, hash_, code, reason):
        outp = (output.handle if output is not None else None)
        _call_rop_func(self.__lib.rnp_key_export_revocation, 0, self.__kid, outp, 0, hash_, code, reason)

    def revoke(self, hash_, code, reason):
        _call_rop_func(self.__lib.rnp_key_revoke, 0, self.__kid, 0, hash_, code, reason)


from .sign import RopSign
