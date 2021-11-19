########################################################################################
###   This file contains R codes to calculate I2C2 of 
###         unbalacned data using trace method
###         2012/12/1 By Haochang, Seonjoo and Ani   
###         revised by Haochang 2013/6/5                        
########################################################################################


I2C2 <- function(y, id = NULL, visit = NULL, J = NULL, I = NULL, p = NULL, 
                 T = NULL, symmetric = FALSE, trun = FALSE, 
                 twoway = TRUE, demean = TRUE) 
{
	
# I2C2                    package:????                    R Documentation
# Description:
#
#     'I2C2' is used to calculate image intraclass correlation coefficient (I2C2) 
#     of balanced/unbalacned data using the trace method
#
# Usage:
#
#     I2C2 <- function(y, id = NULL, visit = NULL, J = NULL, I = NULL, p = NULL, 
#                      T = NULL, symmetric = FALSE, trun = FALSE,
#                      twoway = TRUE, demean = TRUE) 
#     
# Arguments:
# # y: An n by p data matrix containing functional responses. Each row contains measurements 
# #    from a function for one observation at a set of grid points, and each column contains measurements
# #    of all functions at a particular grid point. 
# #    The rows are organized by subjects and then visits, EX) (Y11, Y12, Y21, Y22, ... , YI1 , YI2)
# # I: Number of subjects  
# # J: Number of repetitions
# # id: Vector of IDs, EX) c(1, 1, 2, 2, 3, 3, 4, 4, ... , I, I)
# # visit: Vector of visits, EX) (1, 2, 1, 2, 1, 2, ... , 1, 2)
# # p: dimension of observed vectors Yij (e.g. number of grid points per function), EX) Number of voxels
# # T: Vector of distance (in time) of each visit from baseline visit.
# #	   If the length of time between visits is different for the subjects in the dataset
# #    then match visits according to their distance in time as given by T. 
# #    If T == NULL, match observations from different clusters by visit number
# # twoway: a logical argument indicating whether a oneway or a twoway functional ANOVA (analysis
# #    of variance) decomposition is more appropriate for the problem. "twoway = TRUE" will carry
# #    out twoway ANOVA and remove the visit specific mean
# # demean: if TRUE, include the demean step and output the demeaned dataset
# # symmetric: if FALSE then the function uses the method of moments estimator formula; 
# #    if TRUE, pairwise symmetric sum formula, 
# #    default is FALSE
# # trun: if TRUE, set negative I2C2 to zero
# 
#Output
# # 
# #     The output of the function is a list that contains the following elements. 
# #
# # lambda:       estimated I2C2
# # Kx:           the trace of between-cluster variance operator
# # Ku:           the trace of within-cluster variance operator
# # demean_y:     if demean == TRUE, output the demeaned dataset
#
#Author(s): 
#
#    Haochang Shou, Ani Eloyan, Seonjoo Lee, Vadim Zipunnikov, Mary Beth Nebel, 
#    Brian Caffo, Martin Lindquist, Ciprian M. Crainiceanu     
#
#References:
#
#    Haochang Shou, Ani Eloyan, Seonjoo Lee, Vadim Zipunnikov, Mary Beth Nebel, 
#    Brian Caffo, Martin Lindquist, Ciprian M. Crainiceanu  (2012) The image intra 
#    class correlation coefficient for replication studies.
#
#See Also:
#
#     'I2C2.mcCI', 'I2C2.NullDist'
#				
###     check the missingness of arguments
###     1. Either (id,visit) or (I,J) is needed for identifying clusters. 
###         If both are missing, give error message "not enough information";
###         if only (I,J) is provided, the function would generate (id,visit);
###         if only (id,visit) is provided, the function would generate (I,J);
###     2. If the number of grid points p is missing, the function would generate it.

    if( ( is.null(id) | is.null(visit) ) && ( is.null(I) | is.null(J) ) ) {
        stop("Not enough information! Please provide (id, visit) or (I,J) !")
    }
    
	
	if( !( is.null(I) | is.null(J) ) && !( is.null(id) | is.null(visit) ) ) {    ##both (I,J) and (id,visit) are provided, check consistency of (id, visit)
        
        if((length( unique(id ) ) != I ) | (sum( ( table( id ) != J)) > 0) )
                   stop("Inconsistent information from (id, visit) and (I,J) !") 		
    }
	
	if( !( is.null(I) | is.null(J) ) && ( is.null(id) | is.null(visit) ) ) {    ##only (I,J) fully provided, assume balanced design
        id <- rep(1:I, each = J)
        visit <- rep(1:J, I)
    }
	
	if( ( is.null(I) | is.null(J) ) && !( is.null(id) | is.null(visit) ) ) {    ##only (id,visit) fully provided, check consistency of (id,visit)
        I <- length( unique(id) )
        J <- length( table(visit) )      		
    }
	
	#if (min(table(id))<2) stop("Subjects with no repeats!")
	
    if(is.null(p)){ 
        p <- dim(y)[2]
    }
	
	n <- dim(y)[1]
	y <- matrix(as.numeric(unlist(y)),n,p)  ##Make sure the data matrix is numeric


    
### If demean == TRUE, we calculate the overall mean function and subtract the mean function from the data 
### If twoway functional ANOVA is needed ("twoway==TRUE"),  the visit specific mean function
###     and the deviation from the overall mean to visit specific mean functions are also
###     computed. 

    if( demean == TRUE ) {
       mu <- apply(y, 2, mean)
  	   resd <- matrix(0, nrow = I * J, ncol = p) 
       resd <- t( t(y) - mu ) 
      
       if( twoway == TRUE ) {
	       if( is.null(T) ) {
	     	   T = visit
	       }
		   eta <- matrix(0, length(unique(T)), p)
		   for( j in unique(T) ) {
			   if( sum( T == j ) == 0 ) next
			   if( sum( T ==j ) == 1 ) { 
			  	   eta[ which(unique(T) == j), ] <- as.numeric(unlist(y[T == j,  ])) - mu
			   }else eta[ which(unique(T) == j ), ] <- apply( y[ T == j,  ], 2, mean ) - mu
		   }

	### Calculate residuals by subtracting visit-specific mean from original functions for 
	### 'twoway == TRUE', or subtracting overall mean function for 'twoway == FALSE'. 

		   for( j in unique(T) ) { 
			   if( sum( T == j ) == 0 ) next
		 	   resd[T == j, ] <- t ( t( y[ T == j,  ] ) - (mu + eta[ which( unique(T) == j ), ] ) )
           }				
       }

       W <- resd 
    } 
	
    else {
   	   W <- y
    }

	
    id <- as.numeric( match( id, unique(id) ) ) # reset the id number to be arithmetic sequence starting from 1
    n_I0 = as.numeric( table(id) )  # visit number for each id cluster
	k2 = sum( n_I0^2 )
	Wdd <- colMeans(W)            # population average for the demeaned dataset W
    Si = rowsum(W, id)               # subject-specific sum for the demeaned dataset W

	### If symmetric is FALSE, use the method of moments estimator 
	### formula from the manuscript; otherwise, use pairwise symmetric sum estimator 

	if( symmetric == FALSE ) {
	    Wi = Si / n_I0 
	    trKu <- sum( ( W - Wi[id, ] )^2) / (n - I)
	    trKw <- sum( ( t( W ) - Wdd )^2 ) / (n - 1)
	    trKx <- ( trKw - trKu ) / ( 1 + ( 1 - k2 / n ) / (n - 1) )
    } 
    else {
	    trKu <- ( sum( W^2 * n_I0[id] ) - sum( Si^2 ) ) / (k2 - n)
		trKw <- ( sum( W^2 ) * n - sum( ( n * Wdd )^2 )- trKu * (k2 - n) ) / (n^2 - k2)  
		trKx <-  trKw - trKu	  
	} 
	 
	lambda <- trKx / (trKx + trKu)                     ## estimated I2C2 values
    if( trun == TRUE ) {
    	lambda <- lambda * ( lambda >= 0 )  ## If trun==TRUE, truncate negative lambdas to 0
	}
	
###  Return the results from I2C2 calculation as a list, with 'lambda' as I2C2 value, 
###  Kx and Ku being the trace of between and within cluster variance operators;
###  If demean == TRUE, also return demeaned data 
    
    if( demean == TRUE ) 
       return( list(lambda = lambda, demean_y = resd, Kx = trKx, Ku = trKu) );  
            
    if( demean == FALSE )   
    return( list(lambda = lambda, Ku = trKu, Kx = trKx ) )

} 

