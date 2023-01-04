graph TD
	A[Open Safe]
	AA[Pick Lock]
	AB[Learn Combo]
	ABA[Find Written Combo]
	ABB[Get Combo From Target]
	ABBA[Threaten]
	ABBB[Blackmail]
	ABBC[Eavesdrop]
	ABBCA[Listen to Conversation]
	ABBCB[Get target to state combo]
	ABBD[Bribe]
	AC[Cut Open Safe]
	AD[Install Improperly]
	A --> AA
	A --> AB
	AB --> ABA
	AB --> ABB
	ABB --> ABBA
	ABB --> ABBB
	ABB --> ABBC
	ABBC --> ABBCA
	ABBC --> ABBCB
	ABB --> ABBD
	A --> AC
	A --> AD
	subgraph 0 [ ]
		 ABBCA
		 ABBCB
		 ABBC
	end
