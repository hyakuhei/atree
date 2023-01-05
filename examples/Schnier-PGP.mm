graph TD
	K[Read a message encrypted with PGP]
	KA[Decrypt the message iteself]
	KAA[Break asymmetric encryption]
	KAAA[Brute-force break asymmetric encryption]
	KAAB[Mathematically break asymmetric encryption]
	KAABA[Break RSA]
	KAABB[Factor RSA modulus/calculate ElGamal discrete log]
	KAAC[Cryptanalyze asymmetric encryption]
	KAACA[General cryptanalysis of RSA/ElGaml]
	KAB[Break symmetric key used to encrypt the message via other means]
	KABA[Brute-force symmetric-key encryption]
	KABB[Cryptanalysis of symmetric-key encryption]
	KB[Determine symmetric key used to encrypt the message via other means]
	KBA[Fool sender into encrypting message using public key whos private key is known]
	KBAA[Convince sender that a fake key -with known private- is the key of the intended recipient]
	KBAB[Convince sender to encrypt using more than one-key]
	KBAC[Have the message encrypted with a different public key in the background, unbeknownst to the sender]
	KBB[Have the recipient sign the encrypted symmetric key]
	KBC[Monitor senders computer memory]
	KBD[Monitor receivers computer memory]
	KBE[Determine key from pseudo random number generator]
	KBEA[Determine state of randseed when message was encrypted]
	KBEB[Implant software that alters the state of the randseed]
	KBEC[Implant software that directly affects the choice of symmetric key]
	KBF[Implant software that exposes the symmetric key]
	KC[Get recipient to decrypt message]
	KCA[Chosen ciphertext attack on symmetric key]
	KCB[Chosen ciphertext attack on public key]
	KCC[Send the original message to the recipient]
	KCD[Monitor outgoing mail of recipient]
	KCE[Spoof Reply-to: or From: field of the original message]
	KCF[Read message after it has been decrypted by the recipient]
	KCFA[Copy message off users hard drive or virtual memory]
	KCFB[Copy message off backups]
	KCFC[Monitor network traffic]
	KCFD[Use electromagnetic snooping techniques to read message as it is displayed on the screen]
	KCFE[Recover message from printout]
	KD[Obtain private key of recipient]
	KDA[Factor RSA modulus/calculate ElGamal discrete log]
	KDB[Get private key from recipients key ring]
	KDBA[Obtain encrypted private key ring]
	KDBAA[Copy it from the users hard drive]
	KDBAB[Copy it from backups]
	KDBAC[Monitor network traffic]
	KDBAD[Implant software to expose copy of the private key]
	KDBB[Decrypt private key]
	KDBBA[Break IDEA encryption]
	KDBBAA[Brute-force break IDEA]
	KDBBAB[Cryptanalysis of IDEA]
	KDBBB[Learn passphrase]
	KDBBBA[Monitor keyboard when user types passphrase]
	KDBBBB[Convince user to reveal passphrase]
	KDBBBC[Use keyboard-logging software to record passphrase when typed by user]
	KDBBBD[Guess passphrase]
	KDC[Monitor recipients memory]
	KDD[Implant software to expose private key]
	KDE[Generate insecure public/private keypair for recipient]
	K --> KA
	KA --> KAA
	KAA --> KAAA
	KAA --> KAAB
	KAAB --> KAABA
	KAAB --> KAABB
	KAA --> KAAC
	KAAC --> KAACA
	KA --> KAB
	KAB --> KABA
	KAB --> KABB
	K --> KB
	KB --> KBA
	KBA --> KBAA
	KBA --> KBAB
	KBA --> KBAC
	KB --> KBB
	KB --> KBC
	KB --> KBD
	KB --> KBE
	KBE --> KBEA
	KBE --> KBEB
	KBE --> KBEC
	KB --> KBF
	K --> KC
	KC --> KCA
	KC --> KCB
	KC --> KCC
	KC --> KCD
	KC --> KCE
	KC --> KCF
	KCF --> KCFA
	KCF --> KCFB
	KCF --> KCFC
	KCF --> KCFD
	KCF --> KCFE
	K --> KD
	KD --> KDA
	KD --> KDB
	KDB --> KDBA
	KDBA --> KDBAA
	KDBA --> KDBAB
	KDBA --> KDBAC
	KDBA --> KDBAD
	KDB --> KDBB
	KDBB --> KDBBA
	KDBBA --> KDBBAA
	KDBBA --> KDBBAB
	KDBB --> KDBBB
	KDBBB --> KDBBBA
	KDBBB --> KDBBBB
	KDBBB --> KDBBBC
	KDBBB --> KDBBBD
	KD --> KDC
	KD --> KDD
	KD --> KDE
