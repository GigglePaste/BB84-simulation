# BB84-simulation
This is a simple simulation of BB84 protocol, which is a quantum key distribution protocol. The below is the plot of the accuracy change when a eavesdropper(EVE) is introduced in to the communication protocol between the sender (Alice) and the reciever (Bob). 
![Plot](https://github.com/user-attachments/assets/41d14a3e-2a1e-400f-b07b-d172f06531e5)

BB84 is a quantum key distribution scheme developed by Charles Bennett and Gilles Brassard in 1984.It is the first quantum cryptography protocol.The protocol is provably secure assuming a perfect implementation, relying on two conditions: 
1) the quantum property that information gain is only possible at the expense of disturbing the signal if the two states one is trying to distinguish are not orthogonal (see no-cloning theorem);
2) the existence of an authenticated public classical channel.

It is usually explained as a method of securely communicating a private key from one party to another for use in one-time pad encryption.The proof of BB84 depends on a perfect implementation. Side channel attacks exist, taking advantage of non-quantum sources of information. Since this information is non-quantum, it can be intercepted without measuring or cloning quantum particles. - By Wikipedia

This project was done as a precursor to the actual hardware analogous implementation done under Quantum Experience Lab, R.V. College of Engineering, Bangalore, Karnataka.
