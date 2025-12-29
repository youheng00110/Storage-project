import numpy as np


def build_matrix(id_str: str, n: int = 17) -> np.ndarray:
	digits = [int(ch) for ch in id_str if ch.isdigit()]
	if not digits:
		raise ValueError("学号必须包含至少一位数字")
	seq = []
	power = 1
	while len(seq) < n * n:
		for d in digits:
			expanded = str(d ** power)
			seq.extend(int(c) for c in expanded)
			if len(seq) >= n * n:
				break
		power += 1
	seq = seq[: n * n]
	return np.array(seq, dtype=float).reshape((n, n))


def row_echelon(mat: np.ndarray, tol: float = 1e-10):
	a = mat.astype(float).copy()
	rows, cols = a.shape
	r = 0
	pivot_cols = []
	for c in range(cols):
		pivot = r + np.argmax(np.abs(a[r:, c]))
		if r >= rows or abs(a[pivot, c]) < tol:
			continue
		if pivot != r:
			a[[r, pivot]] = a[[pivot, r]]
		a[r] = a[r] / a[r, c]
		for i in range(r + 1, rows):
			a[i] -= a[i, c] * a[r]
		pivot_cols.append(c)
		r += 1
		if r == rows:
			break
	return a, pivot_cols


def null_space(mat: np.ndarray, tol: float = 1e-12) -> np.ndarray:
	u, s, vt = np.linalg.svd(mat)
	if s.size == 0:
		return np.eye(mat.shape[1])
	rank = np.sum(s > tol * s[0])
	return vt[rank:].T


def full_rank_decomposition(mat: np.ndarray, tol: float = 1e-12):
	u, s, vt = np.linalg.svd(mat, full_matrices=False)
	if s.size == 0:
		return np.zeros_like(mat), np.zeros_like(mat)
	rank = np.sum(s > tol * s[0])
	s_root = np.diag(np.sqrt(s[:rank]))
	b = u[:, :rank] @ s_root
	c = s_root @ vt[:rank, :]
	return b, c


def pivot_columns(mat: np.ndarray, tol: float = 1e-10):
	_, pivots = row_echelon(mat, tol)
	return pivots


def gram_schmidt(vectors: np.ndarray, tol: float = 1e-12) -> np.ndarray:
	basis = []
	for j in range(vectors.shape[1]):
		v = vectors[:, j].astype(float)
		for b in basis:
			v -= np.dot(b, v) * b
		norm = np.linalg.norm(v)
		if norm > tol:
			basis.append(v / norm)
	if not basis:
		return np.empty((vectors.shape[0], 0))
	return np.column_stack(basis)


def inertia_symmetric(mat: np.ndarray, tol: float = 1e-10):
	eigvals = np.linalg.eigvalsh(mat)
	pos = int(np.sum(eigvals > tol))
	neg = int(np.sum(eigvals < -tol))
	zero = eigvals.size - pos - neg
	return pos, neg, zero


def main():
	np.set_printoptions(precision=4, suppress=True)
	id_str = input("请输入学号: ").strip()
	if not id_str:
		raise ValueError("学号不能为空")

	n = 17
	a = build_matrix(id_str, n)
	det_a = np.linalg.det(a)

	echelon, pivots = row_echelon(a)
	null_basis = null_space(a)
	b, c = full_rank_decomposition(a)

	pivot_idxs = pivot_columns(a)
	col_subset = a[:, pivot_idxs] if pivot_idxs else np.empty((n, 0))
	ortho_cols = gram_schmidt(col_subset)

	sym = a + a.T
	inertia = inertia_symmetric(sym)

	print("\nA 矩阵 (17x17):\n", a)
	print("\n|A| =", det_a)
	print("\n行阶梯形矩阵 T:\n", echelon)
	print("主元列索引 (从0开始):", pivots)
	print("\nAx = 0 的零空间基 (列向量):\n", null_basis)
	print("\n满秩分解 A ≈ B @ C，形状 B", b.shape, "C", c.shape)
	print("B:\n", b)
	print("C:\n", c)
	print("\n极大无关列的索引:", pivot_idxs)
	print("极大无关列组成的矩阵:\n", col_subset)
	print("Schmidt 正交化得到的标准正交组 (列向量):\n", ortho_cols)
	print("\nA + A^T 的惯性指数 (正, 负, 零):", inertia)


if __name__ == "__main__":
	main()