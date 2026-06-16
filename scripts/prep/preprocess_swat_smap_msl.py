import os, glob
import numpy as np
import pandas as pd

RAW_ROOT = "/home/mschae/datasets/raw/all_datasets/all_datasets"
OUT_ROOT = "/home/mschae/datasets/processed"

def ensure_2d(x, name):
    x = np.asarray(x)
    if x.ndim == 1:
        x = x[:, None]
    if x.ndim != 2:
        raise ValueError(f"{name} must be 2D after processing, got shape={x.shape}")
    return x.astype(np.float32)

def save_npz(out_path, train, test, label):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    np.savez(out_path,
             train=ensure_2d(train, "train"),
             test=ensure_2d(test, "test"),
             label=np.asarray(label).astype(np.int32))
    print(f"[saved] {out_path}")
    print("  train:", np.asarray(train).shape, "test:", np.asarray(test).shape, "label:", np.asarray(label).shape)

def load_npy_dataset(ds_name):
    ds_dir = os.path.join(RAW_ROOT, ds_name)
    train_path = os.path.join(ds_dir, f"{ds_name}_train.npy")
    test_path  = os.path.join(ds_dir, f"{ds_name}_test.npy")
    label_path = os.path.join(ds_dir, f"{ds_name}_test_label.npy")

    if not (os.path.exists(train_path) and os.path.exists(test_path) and os.path.exists(label_path)):
        raise FileNotFoundError(f"Missing one of: {train_path}, {test_path}, {label_path}")

    train = np.load(train_path)
    test  = np.load(test_path)
    label = np.load(label_path)

    # label은 1D/2D 모두 허용
    label = np.asarray(label)
    if label.ndim == 2 and label.shape[1] == 1:
        label = label[:, 0]
    return train, test, label

def _pick_first(paths):
    return paths[0] if paths else None

def _is_time_col(col):
    c = str(col).lower()
    return ("time" in c) or ("date" in c) or ("timestamp" in c)

def _is_unnamed(col):
    return str(col).lower().startswith("unnamed")

def _label_to_int(y):
    y = pd.Series(y)
    if pd.api.types.is_numeric_dtype(y):
        return (pd.to_numeric(y, errors="coerce").fillna(0).to_numpy() != 0).astype(np.int32)
    s = y.astype(str).str.strip().str.lower()
    attack_words = ["attack", "anomaly", "abnormal", "fault", "1", "true", "yes"]
    normal_words = ["normal", "0", "false", "no"]
    out = np.zeros(len(s), dtype=np.int32)
    for i, v in enumerate(s):
        if any(w == v or w in v for w in attack_words):
            out[i] = 1
        elif any(w == v or w in v for w in normal_words):
            out[i] = 0
        else:
            # 모르는 값이면 숫자 캐스팅 시도
            try:
                out[i] = 1 if float(v) != 0 else 0
            except:
                out[i] = 0
    return out

def _drop_nonfeature_cols(df, extra_drop=None):
    extra_drop = set(extra_drop or [])
    keep = []
    for c in df.columns:
        if _is_unnamed(c) or _is_time_col(c) or c in extra_drop:
            continue
        keep.append(c)
    out = df[keep].copy()

    # 숫자형만 남김
    numeric_cols = [c for c in out.columns if pd.api.types.is_numeric_dtype(out[c])]
    out = out[numeric_cols].copy()
    return out

def load_swat_dataset():
    ds_dir = os.path.join(RAW_ROOT, "SWaT")

    normal_xlsx = os.path.join(ds_dir, "SWaT_Dataset_Normal_v1.xlsx")
    attack_xlsx = os.path.join(ds_dir, "SWaT_Dataset_Attack_v0.xlsx")

    if not (os.path.exists(normal_xlsx) and os.path.exists(attack_xlsx)):
        raise FileNotFoundError(
            f"Expected SWaT xlsx files not found:\n"
            f"  {normal_xlsx}\n"
            f"  {attack_xlsx}"
        )

    # 실제 헤더는 1행
    train_df = pd.read_excel(normal_xlsx, engine="openpyxl", header=1)
    test_df  = pd.read_excel(attack_xlsx, engine="openpyxl", header=1)

    label_candidates = [
        "Normal/Attack",
        "Normal_Attack",
        "label",
        "Label",
        "Attack",
        "attack",
        "anomaly",
        "Anomaly",
    ]

    label_col = None
    for c in test_df.columns:
        if str(c).strip() in label_candidates:
            label_col = c
            break

    if label_col is None:
        raise ValueError(
            f"Could not find SWaT label column in attack xlsx.\n"
            f"Columns = {list(test_df.columns)}"
        )

    y = _label_to_int(test_df[label_col])

    train_x = _drop_nonfeature_cols(train_df)
    test_x  = _drop_nonfeature_cols(test_df, extra_drop=[label_col])

    common = [c for c in train_x.columns if c in test_x.columns]
    if not common:
        raise ValueError("No common numeric feature columns between SWaT train/test.")

    train_x = train_x[common]
    test_x  = test_x[common]

    if len(y) != len(test_x):
        raise ValueError(
            f"SWaT label length mismatch: len(label)={len(y)} vs len(test)={len(test_x)}"
        )

    return train_x.to_numpy(np.float32), test_x.to_numpy(np.float32), y.astype(np.int32)
def main():
    os.makedirs(OUT_ROOT, exist_ok=True)

    # MSL
    train, test, label = load_npy_dataset("MSL")
    save_npz(os.path.join(OUT_ROOT, "MSL", "msl.npz"), train, test, label)

    # SMAP
    train, test, label = load_npy_dataset("SMAP")
    save_npz(os.path.join(OUT_ROOT, "SMAP", "smap.npz"), train, test, label)

    # SWaT
    train, test, label = load_swat_dataset()
    save_npz(os.path.join(OUT_ROOT, "SWaT", "swat.npz"), train, test, label)

if __name__ == "__main__":
    main()
