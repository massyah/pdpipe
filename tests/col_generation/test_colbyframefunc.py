"""Testing ApplyToRows pipeline stages."""

# flake8: noqa: E712

import pytest
import pandas as pd

from pdpipe import ColByFrameFunc
from pdpipe.exceptions import PipelineApplicationError


def _some_df():
    return pd.DataFrame(
        data=[[3, 3], [2, 4], [1, 5]],
        index=[1, 2, 3],
        columns=["A", "B"]
    )


def _are_a_b_equal(df):
    return df['A'] == df['B']


def test_colbyframefunc():
    df = _some_df()
    cbf_stage = ColByFrameFunc('A==B', _are_a_b_equal)
    res_df = cbf_stage(df)
    assert res_df.columns.get_loc('A==B') == 2
    assert res_df['A==B'][1] is True
    assert res_df['A==B'][2] is False
    assert res_df['A==B'][3] is False


def test_colbyframefunc_follow():
    df = _some_df()
    cbf_stage = ColByFrameFunc(
        'A==B', _are_a_b_equal, follow_column='A', func_desc='R')
    res_df = cbf_stage(df)
    assert res_df.columns.get_loc('A==B') == 1
    assert res_df['A==B'][1] is True
    assert res_df['A==B'][2] == False
    assert res_df['A==B'][3] == False


def _are_a_c_equal(df):
    return df['A'] == df['C']


def test_colbyframefunc_error():
    df = _some_df()
    cbf_stage = ColByFrameFunc('A==B', _are_a_c_equal)
    with pytest.raises(PipelineApplicationError):
        cbf_stage(df)
