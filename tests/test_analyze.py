from pathlib import Path
import pandas as pd
from analyze import analyze, OUTPUT_COLUMNS, note_justification

def test_output_schema_and_nonempty():
    df=analyze()
    assert list(df.columns)==OUTPUT_COLUMNS
    assert len(df)>0
    assert df["route"].notna().all()
    assert df["week_of"].notna().all()

def test_deterministic():
    a=analyze()
    b=analyze()
    pd.testing.assert_frame_equal(a,b)

def test_justified_rows_have_note_ids():
    df=analyze()
    justified=df[df["flagged"]=="No (justified)"]
    assert (justified["matched_note_id"].str.len()>0).all()

def test_unexplained_rows_have_no_note_id():
    df=analyze()
    unexplained=df[df["flagged"]=="Yes"]
    assert (unexplained["matched_note_id"]=="").all()
