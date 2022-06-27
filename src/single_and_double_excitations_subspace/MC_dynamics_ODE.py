from hamiltonian.hamiltonian_builder import *


from helper_functions.operators import *
from helper_functions.cloud import *


from single_and_double_excitations_subspace.parameter_generator_for_ODE import *
from single_and_double_excitations_subspace.atomic_contributions_ODE import *
from single_and_double_excitations_subspace.atomic_contributions_optimized_ODE import *


def sandwich_E(r, Beta1D, Beta2D, n, optimized=False):
    # phase vector
    phase = np.exp(-1j*n.T @ r)  # e^{-kvec x r}
    N = len(r)
    if optimized == False:
        s1 = 0
        s2 = 0
        for n in range(N):
            s1 += phase[0, n]*Beta1D[n]
            if Beta2D is not None:  # not Single Excitation
                for m in range(N):
                    for j in range(N):
                        s2 += 4*phase[0, m]*phase.conj()[0, j] * \
                            (Beta2D[n][j].conj()*Beta2D[n][m])

        s = np.abs(s1)**2 + s2
    else:

        # Matrix of difference of phases:
        phases_difference = np.exp(-1j *
                                   (np.reshape(np.subtract.outer(n.T @ r, n.T @ r), [N, N])))
        # First term
        s = np.abs(np.einsum("ij,kj->", np.reshape(Beta1D, [1, N]), phase))**2
        if Beta2D is not None:  # Single Excitation
            # Second term
            s += 4*np.einsum('mj,nj,nm', phases_difference,
                             Beta2D.conj().T, Beta2D)

    return s


def get_Beta1D_projected_state(r, Beta1D_steady_state, Beta2D_steady_state, n1, optimized=False):
    """ 
    Beta1D_steady_state, Beta2D_steady_state are both matrices not time evolution matrices
    """
    phase = np.exp(-1j*n1.T @ r)
    if optimized == False:
        numerator = np.zeros([N], dtype="complex")
        for l in range(N):
            for m in range(N):
                numerator[l] += phase[0, m]*Beta2D_steady_state[l][m]
    else:
        numerator = np.einsum('ij,jk -> i', Beta2D_steady_state, phase.T)

    denominator = np.sqrt(sandwich_E(
        r, Beta1D_steady_state, Beta2D_steady_state, n1))

    return numerator/denominator


def get_g2(r, Beta1D_steady_state, Beta2D_steady_state, Beta1D_tau, Beta2D_tau, n1, n2, optimized=False):
    #g2 = []
    G2 = []
    Inorm = sandwich_E(r, Beta1D_steady_state, Beta2D_steady_state, n2, optimized)
    if Beta2D_tau is None:
        for tau in range(len(Beta1D_tau)):
            G2.append(sandwich_E(r, Beta1D_tau[tau], None, n2, optimized)) 
    else:
        for tau in range(len(Beta1D_tau)):
            G2.append(sandwich_E(r, Beta1D_tau[tau], Beta2D_tau[tau], n2, optimized)) 
    return G2, Inorm


def get_g2_full_MonteCarlo(Omega, Delta, r, t_span_steady_state, R1, R2):
    Beta1D_t, Beta2D_t, t_span, r = SolveForBeta1DandBeta2D(N, kd=None, b0=None, exc_radius=None, Delta=Delta,
                                                            Omega=Omega, wave_mixing=True, scalar=True,
                                                            interaction=True, r=r, t_span=t_span_steady_state)
    tf = 5  # shorter time
    taulist, dt = np.linspace(0, tf, 200, retstep=True)
    Beta1D_steady_state, Beta2D_steady_state = Beta1D_t[-1], Beta2D_t[-1]

    Beta1D_projected_state = get_Beta1D_projected_state(r, Beta1D_steady_state, Beta2D_steady_state,
                                                        R1, optimized=True)
    Beta1D_tau, Beta2D_tau, taulist, r = SolveForBeta1DandBeta2D(N, kd=None, b0=None,
                                                                 exc_radius=None, Delta=Delta,
                                                                 Omega=Omega, wave_mixing=True,
                                                                 scalar=True, interaction=True,
                                                                 r=r, t_span=taulist,
                                                                 initial_Beta1D=Beta1D_projected_state)
    Beta1D_steady_state, Beta2D_steady_state = Beta1D_t[-1], Beta2D_t[-1]

    g2_MonteCarlo = get_g2(r, Beta1D_steady_state, Beta2D_steady_state,
                           Beta1D_tau, Beta2D_tau, R1, R2, optimized=True)

    return g2_MonteCarlo


def get_g2_full_MonteCarlo_saving_everything(Omega, Delta, r, t_span_steady_state, R1, R2):
    Beta1D_t, Beta2D_t, t_span, r = SolveForBeta1DandBeta2D(N, kd=None, b0=None, exc_radius=None, Delta=Delta,
                                                            Omega=Omega, wave_mixing=True, scalar=True,
                                                            interaction=True, r=r, t_span=t_span_steady_state)
    tf = 5  # shorter time
    taulist, dt = np.linspace(0, tf, 200, retstep=True)
    Beta1D_steady_state, Beta2D_steady_state = Beta1D_t[-1], Beta2D_t[-1]

    Beta1D_projected_state = get_Beta1D_projected_state(r, Beta1D_steady_state, Beta2D_steady_state,
                                                        R1, optimized=True)
    Beta1D_tau, Beta2D_tau, taulist, r = SolveForBeta1DandBeta2D(N, kd=None, b0=None,
                                                                 exc_radius=None, Delta=Delta,
                                                                 Omega=Omega, wave_mixing=True,
                                                                 scalar=True, interaction=True,
                                                                 r=r, t_span=taulist,
                                                                 initial_Beta1D=Beta1D_projected_state)
    Beta1D_steady_state, Beta2D_steady_state = Beta1D_t[-1], Beta2D_t[-1]

    g2_MonteCarlo = get_g2(r, Beta1D_steady_state, Beta2D_steady_state,
                           Beta1D_tau, Beta2D_tau, R1, R2, optimized=True)

    return g2_MonteCarlo, Beta1D_steady_state, Beta2D_steady_state, Beta1D_tau, Beta2D_tau, r
