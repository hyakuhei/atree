graph TD
	A[Like writing lists]
	AA[Write a list]
	AB[Read a list]
	AC[Realize you need a tool for the list]
	ACA[Write a tool]
	ACAA[Test the tool]
	ACAB[Publish the tool on GitHub]
	ACB[Realize that you need support for links]
	ACBA[Add the implementation]
	A --> AA
	A --> AB
	A --> AC
	AC --> ACA
	ACA --> ACAA
	ACA --> ACAB
	AC --> ACB
	ACB --> ACBA
	ACBA -.-> ACA
