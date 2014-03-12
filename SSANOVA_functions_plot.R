############################################################################## 
###                         BEGIN FUNCTION CODES                           ###
##############################################################################

# The code in this section was the University of Arizona script 
# "OncePerSessionCode.txt" downloaded from 
# http://apil.arizona.edu/labmanual/index.php?n=Procedures.Statistics on
# November 27, 2007. Modified and commented by Johanna Brugman December 3, 2007.


# This function calculates the smoothing spline fit. To get smoothing
# parameter values, type summary(*)

# First set up the color codes to use.
black0 <- rgb(0,0,0,255,"black0",255)
brown0 <- rgb(123,73,55,255,"brown0",255)
red0 <- rgb(213,13,11,255,"red0",255)
blue0 <- rgb(0,98,172,255,"blue0",255)
gray0<- rgb(108,108,108,255,"gray0",255)
green0 <- rgb(0,151,55,255,"green0",255)
orange0 <- rgb(255,123,0,255,"orange0",255)
gold0 <- rgb(172,181,0,255,"gold0",255)
teal0 <-rgb(0,175,195,255,"teal0",255)

pink0 <-rgb(224,130,180,255,"pink0",255)

purple0 <-rgb(143,72,183,255,"purple0",255)

 # install the necessary package "assist"; comment out next line after initial install
install.packages("assist")

tryCatch(par(family="Doulos SIL"),error=par(family="sans"))

comp<-function(data, word1, word2){

	# Make a subset that includes only the two words being plotted    
	w1w2<-rbind(subset(data, word == word1),subset(data, word == word2));

	# This part normalizes the data to 0 and flips the x and y axes to 
	# facilitate plotting
	
	# Code for switching X to maxX-x

	w1w2$X = max(w1w2$X) - w1w2$X
	# end edgetrak modification


	xmax = max(w1w2$X)
	ymax = max(w1w2$Y)
	w1w2.norm = w1w2
	w1w2.norm$X <- -w1w2$X + xmax
	w1w2.norm$Y <- -w1w2$Y + ymax
       
      
	# This part sets the right levels for the subset being fitted
	a<-levels(w1w2.norm$word)
      word3<-a[a!=word1 & a!=word2]
      levels(w1w2.norm$word)<-list(word1=c(word1,word3),word2=word2)
   
	# This part is the actual fit
	fit.w1w2<-ssr(Y~word*X,rk=list(cubic(X),rk.prod(cubic(X),shrink1(word))),
               data=w1w2.norm,scale=T)
}


# This function plots the the fitted curves and corresponding BCI's in red
# and green
comp.plot<-function(fit,word1,word2,legend1,legend2,color1,color2){
	
      w1<-fit$data[fit$data$word=="word1",]
      w2<-fit$data[fit$data$word=="word2",]
      n1<-nrow(w1)
      ntot<-nrow(w1)+nrow(w2)

	# The model is used to predict values for words 1 and 2
      fit.pred<-predict(fit)
      fit.w1<-data.frame(fit=fit.pred$fit[1:n1],pstd=fit.pred$pstd[1:n1])
      fit.w2<-data.frame(fit=fit.pred$fit[n1+1:ntot],pstd=fit.pred$pstd[n1+1:ntot])

	# The plotting sequence is determined
      order1<-order(w1$X)
      order2<-order(w2$X)

	# The graphing window is set up
	if(Sys.getenv("OS") != "")
	{
	win.graph(width=6,height=4)
	}
	
	par(mar=c(3.5, 3.5, 2.5, 2.5), mgp=c(1.5,0.5,0))
	
	# The size of the plotting area is determined. This is slightly
	# larger than the minimum and maximum numbers so that it'll look nice.
	#xmin = min(fit$data$X)
	#print(min(fit$data$X))
	#xmax = max(fit$data$X)
	#print(max(fit$data$X)) 
	#ymin = min(fit$data$Y) 
	#ymax = max(fit$data$Y)

      # The plotting area is set up
      plot(fit$data$X,fit$data$Y,type="n",xlab="Tongue Length (mm)", ylab="Tongue Height (mm)", 
		xlim=c(0,25), xaxt="s", yaxt="s", ylim=c(0,20), col=1, cex=0.5)

	# The fit and confidence intervals for word 1 are plotted
      lines(w1$X[order1],fit.w1$fit[order1],col=color1,lwd=5,lty=1)
      lines(w1$X[order1],fit.w1$fit[order1]+3*fit.w1$pstd[order1],col=color1,lwd=1,lty=3)
      lines(w1$X[order1],fit.w1$fit[order1]-3*fit.w1$pstd[order1],col=color1,lwd=1,lty=3)
      
	# The fit and confidence intervals for word 2 are plotted
      lines(w2$X[order2],fit.w2$fit[order2],col=color2,lwd=5,lty=4)
      lines(w2$X[order2],fit.w2$fit[order2]+3*fit.w2$pstd[order2],col=color2,lwd=1,lty=3)
      lines(w2$X[order2],fit.w2$fit[order2]-3*fit.w2$pstd[order2],col=color2,lwd=1,lty=3)
      
	# Annotate
	title(paste("AM:",legend1,"vs.",legend2))
	coords <- par("usr");
	legend(coords[1]+70,coords[4]-0,c(legend1,legend2),lwd=5,lty=c(lty=1,lty=4),col=c(color1,color2))
}


# This function plots the Bayes confidence intervals for interaction effects.
# If the BCI's include 0 at a given value of X, then the two curves are similar 
# there.
get.int<-function(fit,word1,word2,legend1,legend2,color1,color2){
	
	op <- par(no.readonly = TRUE) # the whole list of settable par's.
	
      w1<-fit$data[fit$data$word=="word1",]
      w2<-fit$data[fit$data$word=="word2",]
      n1<-nrow(w1)
      ntot<-nrow(w1)+nrow(w2)

	# The model is used to predict values for words 1 and 2
      fit.pred<-predict(fit,terms=c(0,1,0,1,0,1))
      fit.w1<-data.frame(fit=fit.pred$fit[1:n1],pstd=fit.pred$pstd[1:n1])
      fit.w2<-data.frame(fit=fit.pred$fit[n1+1:ntot],pstd=fit.pred$pstd[n1+1:ntot])
      
	# The plotting sequence is determined
	order1<-order(w1$X)
      order2<-order(w2$X)

	# The graphing window is set up
	
	if(Sys.getenv("OS") != "")
	{
	win.graph(width=6,height=6.5)
	}
	
	par(mar=c(3.5, 3.5, 2.5, 2.5), mgp=c(2.4,1,0),mfrow=c(2,1))
	
	
	# Plot the interaction effects for word 1
      ylimits<-c(min(fit.w1$fit[order1]-3*fit.w1$pstd[order1]),
      	max(fit.w1$fit[order1]+3*fit.w1$pstd[order1]))
      plot(fit$data$X,fit.pred$fit,type="n",xlab="X",ylab="Y",ylim=ylimits)
      abline(0,0)
      lines(w1$X[order1],fit.w1$fit[order1],col=color1,lwd=5)
      lines(w1$X[order1],fit.w1$fit[order1]+3*fit.w1$pstd[order1],col=color1,lwd=1,lty=3)
      lines(w1$X[order1],fit.w1$fit[order1]-3*fit.w1$pstd[order1],col=color1,lwd=1,lty=3)
      title(paste("Interaction Effects w/BCI for",legend1))

	# Plot the interaction effects for word 2
      ylimits<-c(min(fit.w2$fit[order2]-3*fit.w2$pstd[order2]),
      	max(fit.w2$fit[order2]+3*fit.w2$pstd[order2]))
      plot(fit$data$X,fit.pred$fit,type="n",xlab="X",ylab="Y",ylim=ylimits)
      abline(0,0)
      lines(w2$X[order2],fit.w2$fit[order2],col=color2,lwd=5)
      lines(w2$X[order2],fit.w2$fit[order2]+3*fit.w2$pstd[order2],col=color2,lwd=1,lty=3)
      lines(w2$X[order2],fit.w2$fit[order2]-3*fit.w2$pstd[order2],col=color2,lwd=1,lty=3)
      title(paste("Interaction Effects w/BCI for",legend2))
      
	list(get.int=fit.pred)
	par(op)


}


# This function combines comp and comp.plot to calculate and plot the fit
# in red and green
compare<-function(data,w1,w2,wl1,wl2){
	sepsp.t1<-comp(data=data,w1,w2)
	comp.plot(sepsp.t1,w1,w2,wl1,wl2,red0,green0)
}


# This function combines comp and comp.plot to calculate and plot the fit
# in grayscale
comparegray<-function(data,w1,w2,wl1,wl2,output='screen'){
	sepsp.t1<-comp(data=data,w1,w2)
	comp.plot(sepsp.t1,w1,w2,wl1,wl2,black0,gray0)
}


# This function combines comp and interaction.bci to calculate the fit and
# plot the interactions
compareBCI<-function(data,w1,w2,wl1,wl2){
	sepsp.t1<-comp(data=data,w1,w2)
	interaction.bci<-get.int(sepsp.t1,w1,w2,wl1,wl2,red0,green0)
}


# This function combines comp and comp.plot to make a PDF of the plot
comparepdf<-function(data,w1,w2,wl1,wl2){
	pdf(paste(w1,' ',w2,'.pdf',sep=''));
	sepsp.t1<-comp(data=data,w1,w2)
	comp.plot(sepsp.t1,w1,w2,wl1,wl2,red0,green0)
}

library(assist)

###############################################################################
###                           END FUNCTION CODES                            ###
###############################################################################


###############################################################################
###                           BEGIN PLOTTING                                ###
###############################################################################

#### #### IF USING R SCRIPT(S) FROM AUTOGROUPER.PY, REPLACE THE BELOW #### ####
#### ####       (you can add as many in a row as you would like)      #### ####

if(Sys.getenv("OS") != "")
{
  my.Filters = matrix(c("TXT files (*.TXT)","All files (*.*)","*.TXT","*.*"),2,2);
  input.traces = choose.files(caption="Select .txt files (multiple selection allowed)",filters=my.Filters);
} else 
{
  input.traces = file.choose(new=FALSE);
}

# The working directory is set to the folder that contains the TXT files by finding 
# the last "\" and selecting a substring that stops there. 
not.found = TRUE;
search.index = nchar(input.traces[1]);
while(not.found && search.index >= 1){
  if(substring(input.traces[1],search.index,search.index)=="\\" | substring(input.traces[1],search.index,search.index)=="/"){
    not.found = FALSE;
  }else{
    search.index = search.index-1;
  }
}
my.Default = substring(input.traces[1],1,search.index);
setwd(my.Default);

# Filenames without the path are listed in the vector "input.traces.filenames".
input.traces.filename = substring(input.traces,search.index+1,nchar(input.traces))


# Read in the data

mydata = read.table(input.traces.filename,h=T,quote="\"",dec=".", fill = TRUE, comment.char="")
mydata <- as.data.frame(mydata)

# Enter the labels for the three things you want to compare
#compare(mydata,"B2","B3", "B4", "B5")

