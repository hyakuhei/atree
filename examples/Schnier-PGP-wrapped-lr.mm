graph LR
	K[Read a message\nencrypted with\nPGP]
	KA[Decrypt the message\niteself]
	KAA[Break asymmetric\nencryption]
	KAAA[Brute-force break\nasymmetric encryption]
	KAAB[Mathematically\nbreak asymmetric\nencryption]
	KAABA[Break RSA]
	KAABB[Factor RSA modulus/calculate\nElGamal discrete\nlog]
	KAAC[Cryptanalyze asymmetric\nencryption]
	KAACA[General cryptanalysis\nof RSA/ElGaml]
	KAB[Break symmetric\nkey used to encrypt\nthe message via\nother means]
	KABA[Brute-force symmetric-key\nencryption]
	KABB[Cryptanalysis of\nsymmetric-key encryption]
	KB[Determine symmetric\nkey used to encrypt\nthe message via\nother means]
	KBA[Fool sender into\nencrypting message\nusing public key\nwhos private key\nis known]
	KBAA[Convince sender\nthat a fake key\n-with known private-\nis the key of the\nintended recipient]
	KBAB[Convince sender\nto encrypt using\nmore than one-key]
	KBAC[Have the message\nencrypted with\na different public\nkey in the background,\nunbeknownst to\nthe sender]
	KBB[Have the recipient\nsign the encrypted\nsymmetric key]
	KBC[Monitor senders\ncomputer memory]
	KBD[Monitor receivers\ncomputer memory]
	KBE[Determine key from\npseudo random number\ngenerator]
	KBEA[Determine state\nof randseed when\nmessage was encrypted]
	KBEB[Implant software\nthat alters the\nstate of the randseed]
	KBEC[Implant software\nthat directly affects\nthe choice of symmetric\nkey]
	KBF[Implant software\nthat exposes the\nsymmetric key]
	KC[Get recipient to\ndecrypt message]
	KCA[Chosen ciphertext\nattack on symmetric\nkey]
	KCB[Chosen ciphertext\nattack on public\nkey]
	KCC[Send the original\nmessage to the\nrecipient]
	KCD[Monitor outgoing\nmail of recipient]
	KCE[Spoof Reply-to:\nor From: field\nof the original\nmessage]
	KCF[Read message after\nit has been decrypted\nby the recipient]
	KCFA[Copy message off\nusers hard drive\nor virtual memory]
	KCFB[Copy message off\nbackups]
	KCFC[Monitor network\ntraffic]
	KCFD[Use electromagnetic\nsnooping techniques\nto read message\nas it is displayed\non the screen]
	KCFE[Recover message\nfrom printout]
	KD[Obtain private\nkey of recipient]
	KDA[Factor RSA modulus/calculate\nElGamal discrete\nlog]
	KDB[Get private key\nfrom recipients\nkey ring]
	KDBA[Obtain encrypted\nprivate key ring]
	KDBAA[Copy it from the\nusers hard drive]
	KDBAB[Copy it from backups]
	KDBAC[Monitor network\ntraffic]
	KDBAD[Implant software\nto expose copy\nof the private\nkey]
	KDBB[Decrypt private\nkey]
	KDBBA[Break IDEA encryption]
	KDBBAA[Brute-force break\nIDEA]
	KDBBAB[Cryptanalysis of\nIDEA]
	KDBBB[Learn passphrase]
	KDBBBA[Monitor keyboard\nwhen user types\npassphrase]
	KDBBBB[Convince user to\nreveal passphrase]
	KDBBBC[Use keyboard-logging\nsoftware to record\npassphrase when\ntyped by user]
	KDBBBD[Guess passphrase]
	KDC[Monitor recipients\nmemory]
	KDD[Implant software\nto expose private\nkey]
	KDE[Generate insecure\npublic/private\nkeypair for recipient]
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
