graph TD
	A[Like writing lists]
	AA[Write a list]
	AB[Read a list]
	AC[Realize you need a tool for the list]
	ACA[Write a tool]
	ACAB[Test the tool]
	ACAC[Publish the tool on GitHub]
	ACAD[Realize that you need support for links]
	ACAE[Add the implementation]
	A --> AA
	A --> AB
	A --> AC
	AC --> ACA
	ACA --> ACAB
	ACA --> ACAC
	ACA --> ACAD
	ACA --> ACAE
	ACAE --> ACA
