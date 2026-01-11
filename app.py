# app.py
import streamlit as st
from qiskit import IBMQ, QuantumCircuit, Aer, execute
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quantum Neuromorphic Demo", layout="wide")
st.title("Quantum Neuromorphic Spike Demo")
st.write("Real-time quantum entropy perturbs spike timing in a neuromorphic system.")

# --------------------------
# IBM Quantum API Key
# --------------------------
api_key = st.text_inputXVBHS5-G8Df0coEb7TAXTSUFV6kLln0NVCPXtL7D2eak
, type="password")

if api_key:
    IBMQ.save_account(api_key, overwrite=True)
    provider = IBMQ.load_account()
    st.success("Connected to IBM Quantum!")

    # --------------------------
    # Parameters
    # --------------------------
    n_qubits = st.slider("Number of Qubits", 2, 10, 5)
    shots = st.slider("Number of Quantum Samples", 5, 50, 20)

    # --------------------------
    # Build quantum circuit
    # --------------------------
    qc = QuantumCircuit(n_qubits, n_qubits)
    for q in range(n_qubits):
        qc.h(q)
    qc.measure(range(n_qubits), range(n_qubits))

    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend=backend, shots=shots)
    result = job.result()
    counts = result.get_counts(qc)

    # --------------------------
    # Convert to spike jitter
    # --------------------------
    bit_sequence = []
    for outcome, count in counts.items():
        bits = [int(b) for b in outcome]
        bit_sequence.extend(bits * count)
    jitter = np.array(bit_sequence) * 0.005
    base_spikes = np.linspace(0, 1, len(jitter))
    perturbed_spikes = base_spikes + jitter

    # --------------------------
    # Plot in Streamlit
    # --------------------------
    st.subheader("Neuromorphic Spike Timing")
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.eventplot([base_spikes], lineoffsets=1, colors='blue', label='Original')
    ax.eventplot([perturbed_spikes], lineoffsets=0.5, colors='red', label='Quantum Perturbed')
    ax.set_xlabel("Time (s)")
    ax.legend()
    st.pyplot(fig)
else:
    st.info("Enter your IBM Quantum API key to start the demo.")
