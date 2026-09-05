# Approach

## Mathematical idea

We are given a pair of parametric equations where both \(x\) and \(y\) depend
on \(t\):

\[
x=t\cos\theta-e^{M|t|}\sin(0.3t)\sin\theta+X
\]

\[
y=42+t\sin\theta+e^{M|t|}\sin(0.3t)\cos\theta.
\]

The values of \(\theta\), \(M\), and \(X\) are unknown. We are given the
resulting \((x,y)\) points, but not the value of \(t\) that generated each
point. This missing \(t\) is the main difficulty.

Since \(6<t<60\), \(t\) is always positive and therefore \(|t|=t\).

In addition to this, it is observed that the \(e^{Mt}\sin(0.3t)\) term is
present in both \(x\) and \(y\). Thus, we can write

\[
q(t)=e^{Mt}\sin(0.3t).
\]

The equations now become

\[
x-X=t\cos\theta-q(t)\sin\theta
\]

\[
y-42=t\sin\theta+q(t)\cos\theta.
\]

We can now rewrite these equations in matrix form:

\[
\begin{pmatrix}x-X\\y-42\end{pmatrix}
=
\begin{pmatrix}
\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta
\end{pmatrix}
\begin{pmatrix}t\\q(t)\end{pmatrix}.
\]

The interpretation of this matrix is that the point \((t,q(t))\) is rotated by
\(\theta\) and then shifted by \((X,42)\).

Therefore, for any proposed values of \(\theta\) and \(X\), I can undo the
rotation by applying the inverse rotation matrix \(R(-\theta)\) to the shifted
data point:

\[
\begin{pmatrix}\hat t_i\\\hat q_i\end{pmatrix}
=
\begin{pmatrix}
\cos(-\theta)&-\sin(-\theta)\\
\sin(-\theta)&\cos(-\theta)
\end{pmatrix}
\begin{pmatrix}x_i-X\\y_i-42\end{pmatrix}.
\]

Expanding this matrix gives an independently recovered value of \(t\) and
\(q(t)\) for every supplied point:

\[
\hat t_i=(x_i-X)\cos\theta+(y_i-42)\sin\theta
\]

\[
\hat q_i=-(x_i-X)\sin\theta+(y_i-42)\cos\theta.
\]

If the proposed \(\theta\), \(M\), and \(X\) are correct, the independently
recovered \(\hat q_i\) must be almost equal to the value predicted using
\(\hat t_i\):

\[
q_{\text{pred},i}=e^{M\hat t_i}\sin(0.3\hat t_i).
\]

The error, also called the residual, for each point is

\[
r_i=\hat q_i-q_{\text{pred},i},
\]

and the loss I minimize is the mean absolute residual:

\[
L(\theta,M,X)=\frac{1}{N}\sum_{i=1}^{N}|r_i|.
\]

Programmatically, we can define an optimizer to reduce this L1 loss and recover
the unknown parameters.

## Programmatic approach

- **Data Input** - The program reads all the points from `xy_data.csv`. The
  order of the rows does not matter because each point is handled independently.

- **Residual Calculation** - The `inverse_residuals` function takes a candidate
  \((\theta,M,X)\), calculates \(\hat t\), \(\hat q\), and the predicted \(q\),
  and returns the residuals.

- **Objective Function** - The `objective` function converts the residuals into
  one L1 loss value. It also adds a penalty if an inferred \(\hat t\) falls
  outside \([6,60]\), preventing solutions that violate the given range.

- **Parameter Optimization** - Differential evolution searches for the
  parameters using a population of candidates within the given bounds. It
  repeatedly mutates and combines them, evaluates their loss, and keeps the
  better results. This is useful because the sine term can create multiple local
  minima. SciPy also polishes the best candidate locally by default, while a
  fixed random seed makes the result reproducible.

- **Result Output** - The program recalculates the mean L1 residual without the
  range penalty and writes \(\theta\), \(M\), \(X\), and the loss to
  `result.json`.

## Result

The recovered values are

\[
\theta=29.999973^\circ,\qquad
M=0.0299999974,\qquad
X=54.9999982,
\]

with a mean L1 loss of

\[
2.5598\times10^{-6}.
\]

The very small loss and the numerical values indicate the clean solution

\[
\boxed{\theta=30^\circ,\qquad M=0.03,\qquad X=55}.
\]


