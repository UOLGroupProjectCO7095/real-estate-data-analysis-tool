COCOMO I – Software Cost Estimation

1. Introduction

For our Real Estate Data Collection and Analysis Tool project, we have used the COCOMO I model to estimate the development effort and time required to complete the software.

COCOMO (Constructive Cost Model) is a software estimation technique developed by Barry Boehm. It helps estimate how much effort, time and staffing may be needed to develop a software system.

In this section, I have applied the Basic COCOMO I model to our complete project.

2. Project Details
Attribute	Description
Project Name-Real Estate Data Collection and Analysis Tool
EstimationTechnique-BasicCOCOMO I
Project Mode - we have used Organic
Estimated Project Size	4 KLOC
Team Members	4 

Project size assumption: For this estimation, we have assumed the project size to be 4 KLOC (4,000 lines of code). This is an estimated value used for the calculation and is 
not based on an actual code count(it's just an estimation.

3. Selection of Project Mode

We have selected the Organic mode for this project because it is a relatively small software system with 
manageable requirements.

The project involves collecting property information, processing data, managing property records and presenting results 
through analysis and visualizations. These functions are being developed using familiar tools and technologies.

Therefore, Organic mode is a reasonable assumption for this initial estimation.

4. COCOMO I Formulas

For the Organic project mode, the Basic COCOMO I model uses the following formulas:

Effort estimation:

E(Effort) = 2.4 × (KLOC)^1.05

Development time estimation:

D = 2.5 × (Effort)^0.38

Average team size:

Average Team Size (P) = Effort / Development Time

Where:

* E represents the estimated effort in person-months.
* D represents the estimated development time in months.
* KLOC represents thousands of lines of code.
* P represents the persons required for development. 

5. Effort Estimation

For our project, the assumed size is 4 KLOC.
Using the Organic mode formula:
E = 2.4 × (4)^1.05
E = 2.4 × 4.287
Estimated Effort = 10.29 Person-Months
It means the project is estimated to require approximately 10.29 person-months 
of development effort.
6. Development Time Estimation
After calculating the effort, next step is to estimate the development time.

D = 2.5 × (10.29)^0.38

Estimated Development Time = 6.06 Months

Based on this calculation, the estimated development period is approximately six months.

7. Average Team Size
The average number of people required can be estimated by dividing the total effort by the development time.

Average Team Size = 10.29 / 6.06

Average Team Size = 1.70 Persons

This suggests that approximately two people would be required on average according to the model.

8. Final Estimation Results

The following table shows the results obtained using Basic COCOMO I.

Parameters	Estimated Results
Project Size	4 KLOC
Development Effort	10.29 Person-Months
Development Time	6.06 Months
Average Team Size	1.70 Persons

9. Conclusion

Using the Basic COCOMO I model, we estimated the effort and development time required for our Real Estate Data Collection and Analysis Tool.

Based on the assumed project size of 4 KLOC, the estimated effort is 10.29 person-months, and the development time is approximately 6.06 months.

This estimation gives us an initial idea of the resources and time that may be required to complete the project. The actual development time may differ depending on the 
complexity of the tasks, team experience and project progress.

The estimated values will also be useful when comparing the results of COCOMO I with COCOMO II.