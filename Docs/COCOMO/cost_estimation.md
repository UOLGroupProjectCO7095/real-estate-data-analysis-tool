Comparison between COCOMO I and COCOMO II
1. Introduction
For our Real Estate Data Collection and Analysis Tool, we have used two software estimation models: COCOMO I and COCOMO II.
The main purpose of using both models is to estimate the effort and time needed to develop the project and understand how their results are different. 
Though both models are used for software cost estimation, they follow slightly different approaches. COCOMO, we use a simpler method for estimation method, whereas COCOMO II considers additional factors are PREC, FLEX, RESL, TEAM, PMAT and also additional effort multipliers RCPX, RUSE, PDIF, PERS, PREX, FCIL, SCED that can affect software development.
2. Comparison of COCOMO I And COCOMO II Estimation results are 
The following table shows the results obtained from both estimation models.
Parameter-COCOMO I-COCOMO II
Project Size-4 KLOC-4 KSLOC
Project Mode-Organic-Early Design
Estimated Effort-10.29 Person-Months-13.52 Person-Months
Development Time-6.06 Months-8.49 Months
Average Team Size-1.70 Persons-1.59 Persons
We have taken project size of 4 KLOC (4 KSLOC) is an assumed value used for this estimation code, rather than the measurement code. 
3. Differences Between the Two Models
COCOMO I is a relatively straightforward model. It uses the estimated project size and development mode to calculate the effort and time required. For our project, the Organic mode was selected because the software has manageable requirements and functionality.
COCOMO II provides a more detailed approach to estimation. In addition to project size, it considers factors such as team capability, project complexity, development environment and personnel experience.
This means COCOMO II takes more project conditions compare to COCOMO I in account of when estimating the development effort.
4. Discussion of the Results
From the calculations, COCOMO we have estimated the development effort at 10.29 person-months, while COCOMO II estimated 13.52 person-months.
The COCOMO II estimate is higher because it uses a different estimation approach and considers additional project-related factors.

The estimated development time also differs. COCOMO, it gives approximately 6.06 months, whereas COCOMO II gives approximately 8.49 months.
The results show that the choice of estimation model can influence the predicted effort and development time. However, both results are estimates rather than exact predictions of how long the project will take.
5. Limitations of the Estimation
One limitation of this estimation is that the project size was assumed to be 4 KLOC instead of being calculated from the actual source code.
The scale factors and effort multiplier ratings used in COCOMO II were also selected based on the available project information.
Therefore, the results may change if more accurate project size information or different factor ratings are used.
6. Conclusion
After applying both COCOMO I and COCOMO II to our Real Estate Data Collection and Analysis Tool, I found that the two models produced different estimates for development effort and time.
COCOMO we  provided a simpler calculation, while COCOMO II considered additional factors related to the project and development team.
For this estimation, COCOMO II produced a higher effort and development time estimate than COCOMO I.
Using both models helped me understand how software development effort can be estimated in different ways and why it is important to consider project characteristics when planning software development.
These estimates provide an initial understanding of the resources required for the project. They should not be treated as the actual time taken to complete our three Scrum sprints.