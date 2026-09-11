from dataclasses import dataclass
import pandas as pd


def classify_hidden_commitment(q_now, v_future, tol=1e-12):
    return bool(q_now <= tol and v_future > tol)


def compare_decision_objects(rows):
    df = pd.DataFrame(rows)
    df["hidden_commitment"] = (df["present_requirement"] <= 0.0) & (df["unavoidable_future_volume"] > 0.0)
    df["present_viability_loss"] = ~df["current_policy_feasible"]
    df["future_viability_loss"] = ~df["future_policy_feasible"]
    df["tipping_point"] = df["adaptation_threshold_crossed"]
    df["real_option_signal"] = df["replacement_option_value"] > 0.0
    df["robust_control_failure"] = ~df["robust_policy_feasible"]
    return df


def separability_witnesses():
    rows = [
        dict(case="HDC_without_present_viability_loss", present_requirement=0.0, unavoidable_future_volume=2.0,
             current_policy_feasible=True, future_policy_feasible=False, adaptation_threshold_crossed=False,
             replacement_option_value=0.0, robust_policy_feasible=False),
        dict(case="tipping_without_HDC", present_requirement=0.0, unavoidable_future_volume=0.0,
             current_policy_feasible=True, future_policy_feasible=True, adaptation_threshold_crossed=True,
             replacement_option_value=0.0, robust_policy_feasible=True),
        dict(case="option_value_without_HDC", present_requirement=0.0, unavoidable_future_volume=0.0,
             current_policy_feasible=True, future_policy_feasible=True, adaptation_threshold_crossed=False,
             replacement_option_value=1.0, robust_policy_feasible=True),
        dict(case="robust_failure_without_HDC", present_requirement=0.0, unavoidable_future_volume=0.0,
             current_policy_feasible=True, future_policy_feasible=True, adaptation_threshold_crossed=False,
             replacement_option_value=0.0, robust_policy_feasible=False),
        dict(case="visible_deficit_not_hidden", present_requirement=1.0, unavoidable_future_volume=2.0,
             current_policy_feasible=False, future_policy_feasible=False, adaptation_threshold_crossed=True,
             replacement_option_value=1.0, robust_policy_feasible=False),
    ]
    return compare_decision_objects(rows)


def overlap_matrix():
    return pd.DataFrame([
        ["Hidden commitment", "Q_now=0 AND V_future^U>0", "future unavoidable replacement while present need is zero", "target object"],
        ["Viability kernel", "existence of admissible trajectory satisfying constraints", "state/control feasibility", "overlap but not definitionally identical"],
        ["Backward reachability", "states leading to target/failure set", "future set reachability", "overlap but HDC adds zero-present-need and burden magnitude"],
        ["Adaptation tipping point", "current strategy ceases to meet objectives", "strategy expiry", "not definitionally identical"],
        ["Real options", "economic value of flexibility", "timing/value of options", "different objective"],
        ["Robust control", "policy satisfying objectives over uncertainty set", "robust feasibility", "not definitionally identical"],
        ["Water-system planning", "least-cost/reliable future portfolio", "portfolio/cost/reliability", "can contain HDC ingredients but not same predicate"],
    ], columns=["framework", "defining_object", "primary_question", "relation_to_HDC"])
