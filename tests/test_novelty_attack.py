from dct.novelty.hidden_commitment import classify_hidden_commitment, separability_witnesses


def test_hidden_commitment_predicate():
    assert classify_hidden_commitment(0.0, 1.0)
    assert not classify_hidden_commitment(1.0, 1.0)
    assert not classify_hidden_commitment(0.0, 0.0)


def test_separability_witnesses():
    df = separability_witnesses()
    assert ((df.hidden_commitment) & (~df.present_viability_loss)).any()
    assert ((df.tipping_point) & (~df.hidden_commitment)).any()
    assert ((df.real_option_signal) & (~df.hidden_commitment)).any()
    assert ((df.robust_control_failure) & (~df.hidden_commitment)).any()
