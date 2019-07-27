from .ssz_test_case import invalid_test_case, valid_test_case
from eth2spec.utils.ssz.ssz_typing import boolean, uint8, uint16, uint32, uint64, uint128, uint256, Vector, BasicType
from eth2spec.utils.ssz.ssz_impl import serialize
from random import Random
from typing import Dict
from eth2spec.debug.random_value import RandomizationMode, get_random_ssz_object


def basic_vector_case_fn(rng: Random, mode: RandomizationMode, elem_type: BasicType, length: int):
    return get_random_ssz_object(rng, Vector[elem_type, length],
                                 max_bytes_length=length * 8,
                                 max_list_length=length,
                                 mode=mode, chaos=False)


BASIC_TYPES: Dict[str, BasicType] = {
    'bool': boolean,
    'uint8': uint8,
    'uint16': uint16,
    'uint32': uint32,
    'uint64': uint64,
    'uint128': uint128,
    'uint256': uint256
}


def valid_cases():
    rng = Random(1234)
    for (name, typ) in BASIC_TYPES.items():
        for length in [1, 2, 3, 4, 5, 8, 16, 31, 512, 513]:
            for mode in [RandomizationMode.mode_random, RandomizationMode.mode_zero, RandomizationMode.mode_max]:
                yield f'vec_{name}_{length}_{mode.to_name()}',\
                      valid_test_case(lambda: basic_vector_case_fn(rng, mode, typ, length))


def invalid_cases():
    # zero length vectors are illegal
    for (name, typ) in BASIC_TYPES:
        yield f'vec_{name}_0', lambda: b''

    rng = Random(1234)
    for (name, typ) in BASIC_TYPES.items():
        for length in [1, 2, 3, 4, 5, 8, 16, 31, 512, 513]:
            yield f'vec_{name}_{length}_nil', invalid_test_case(lambda: b'')
            for mode in [RandomizationMode.mode_random, RandomizationMode.mode_zero, RandomizationMode.mode_max]:
                yield f'vec_{name}_{length}_{mode.to_name()}_one_less', \
                      invalid_test_case(lambda: serialize(basic_vector_case_fn(rng, mode, typ, length - 1)))
                yield f'vec_{name}_{length}_{mode.to_name()}_one_more', \
                      invalid_test_case(lambda: serialize(basic_vector_case_fn(rng, mode, typ, length + 1)))
