COCOMO II – Software Cost Estimation
1. Introduction
For our Real Estate Data Collection and Analysis Tool, we have also applied the COCOMO II model to estimate the development
effort and time required for the project.
COCOMO II is an updated version of the original COCOMO model. It 
considers different factors that can affect software development, 
such as project complexity, team experience, technology and development conditions.

This model provides another way to estimate the resources needed to complete our project.

2. Project Details

Attributes	Description
Project Name-Real Estate Data Collection and Analysis Tool
Estimation Model is COCOMO II
Estimation Approach	Early Design
Estimated Project Size is4 KSLOC
Team Members are 4

Project size assumption: The project size is estimated at 4 KSLOC 
(4,000 lines of code). This is an assumed value for estimation purposes, not an actual 
measurement of the source code.
3. COCOMO II Estimation Approach
For this project, we have selected the Early Design model because it is suitable for making 
an initial estimate when the project is understood but detailed implementation information is not required.
COCOMO II considers scale factors and effort multipliers when calculating the development effort.
4. COCOMO II Formula
The effort estimation formula is:
5. COCOMO 1_ Effort Edtimation
E= a*(KLOC)^b
E= Development effort (person-Months)
a and b are constants
KLOC= Kilo lines of code
For Organic Mode:
E=2.4x(KLOC)^1.05
COCOMO II Formula
PM = 2.94 x(KLOC)^E X EM
PM= Development effort (persons-months)
KSLOC= Thousands of Source Lines of Code
E= Scale Exponent
EM= Product of effort multipliers
PM = 2.94 × (KSLOC)^E × EM

The scale exponent is calculated using:
E = 0.91 + 0.01 × ΣSF
Where ΣSF represents the total of the five scale factors.
5. The Scale Factors are 

For this estimation, the following scale factor ratings have been assumed.
Scale Factor	Rating	Explanation
Precedentedness (PREC)-Nominal	The project uses familiar software development concepts.
Development Flexibility (FLEX)-Nominal	The team has some flexibility in implementation.
Architecture and Risk Resolution (RESL)-Nominal	The project has a defined structure and manageable risks.
Team Cohesion (TEAM)-Nominal	The team works together to complete project tasks.
Process Maturity (PMAT)-Nominal	Standard development practices are followed.
For the calculation, the assumed nominal scale-factor values are:
PREC = 3.72
FLEX = 3.04
RESL = 4.24
TEAM = 3.29
PMAT = 4.68
Total scale factors:
ΣSF = 3.72 + 3.04 + 4.24 + 3.29 + 4.68
ΣSF = 18.97
Therefore:
E = 0.91 + (0.01 × 18.97)
E = 1.0997
6. Effort Multipliers

For this initial estimation, all seven Early Design effort multipliers are assumed to have nominal ratings.
Effort Multiplier	Rating
6. Effort Multipliers
| Factor | Description | Selected Rating | Effort Multiplier |
| RCPX | Product reliability and complexity | Nominal | 1.00 |
| RUSE | Required software reuse | Nominal | 1.00 |
| PDIF | Platform difficulty | Nominal | 1.00 |
| PERS | Personnel capability | Nominal | 1.00 |
| PREX | Personnel experience | Nominal | 1.00 |
| FCIL | Facilities and development tools | Nominal | 1.00 |
| SCED | Required development schedule | Nominal | 1.00 |
All seven Early Design effort multipliers are assigned
nominal ratings for this initial estimation.
A nominal multiplier of 1.00 is used for each factor.
Therefore, the combined effort multiplier is:
EM = 1.00 × 1.00 × 1.00 × 1.00 × 1.00 × 1.00 × 1.00
EM = 1.00
These ratings are initial assumptions based on the
available project information. They can be reviewed
when more detailed project information becomes available.
The ratings were selected by considering the team’s experience, project functionality, size of the property dataset and documentation requirements.
These selections are assumptions for the estimation exercise and may be adjusted if further project information becomes available.
The numerical effort multiplier values will be obtained from the corresponding COCOMO II rating tables before calculating the final effort.
Then we can calculate the correct effort multiplier (EM) estimated effort is EM = 1.00.
7. Effort Calculation
Using the COCOMO II formula:
PM = 2.94 × (KSLOC)^E × EM
PM = 2.94 × (4)^1.0997 × 1.00
Estimated Effort ≈ 13.52 Person-Months
8. Development Time Estimation
For this initial estimation, the COCOMO II schedule equation is:
TDEV = 3.67 × (PM)^F
Where:
F = 0.28 + 0.2 × (E - 0.91)
F = 0.28 + 0.2 × (1.0997 - 0.91)
F = 0.31794
Therefore:
TDEV = 3.67 × (13.52)^0.31794
Estimated Development Time ≈ 8.49 Months
9. Average Team Size
Average Team Size = Effort / Development Time
Average Team Size = 13.52 / 8.49
Average Team Size ≈ 1.59 Persons
10. Final Estimation Results
Parameter	Estimated Result
Project Size	4 KSLOC
Scale Exponent	1.0997
Effort Multiplier	1.00
Estimated Effort	13.52 Person-Months
Development Time	8.49 Months
Average Team Size	1.59 Persons
11. Conclusion
Using the COCOMO II model, I estimated the effort and development time for our Real Estate Data Collection and Analysis Tool.
Based on the assumed project size of 4 KSLOC and the selected nominal ratings, the estimated development effort is approximately 13.52 person-months. The estimated development time is around 8.49 months.
This model considers additional project factors compared with COCOMO I, which helps provide a more detailed estimation. However, the results depend on the assumptions made for project size, scale factors and effort multipliers.
These estimates will be compared with the COCOMO results to understand the differences between the two models.