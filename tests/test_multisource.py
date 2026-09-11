from dct.multisource import unavoidable_replacement

def test_multisource_nonnegative():
    q = unavoidable_replacement(1.0,[0.4,0.4],[0.08,0.08],0.08,[0.1,0.1])
    assert q >= 0
