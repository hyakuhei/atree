graph TD
	K[Open Safe]
	KA[Pick Lock]
	KB[Learn Combo]
	KC[Cut Open Safe]
	KD[Install Improperly]
	KBA[Find Written Combo]
	KBB[Get Combo From Target]
	KBBA[Threaten]
	KBBB[Blackmail]
	KBBC[Eavesdrop]
	KBBD[Bribe]
	KBBCA[Listen to Conversation]
	KBBCB[Get target to state combo]
	K --> KA
	K --> KB
	K --> KC
	K --> KD
	KB --> KBA
	KB --> KBB
	KBB --> KBBA
	KBB --> KBBB
	KBB --> KBBC
	KBB --> KBBD
	KBBC --> KBBCA
	KBBC --> KBBCB
	subgraph 0 [ ]
		 KBBCA
		 KBBCB
		 KBBC
	end
