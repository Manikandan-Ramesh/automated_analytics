class derived_columns:
     def __init__(self,df):
        self.df=df
        
     def create_derived_columns(self):
            """To create derived columns using arithmetic operations given by the user"""
            str1=" "
            f=1
            datecol=[x for x in self.df.columns if self.df[x].dtypes=='datetime64[ns]']
            cont = [x for x in self.df.columns if self.df[x].dtypes != 'object' and x not in datecol]
            cat=[x for x in self.df.columns if self.df[x].dtypes == 'object' and x not in datecol]
    
            while(f==1):
                str1=input("Enter + to sum columns - to subtract * to multiply and / to divide or enter 0 to exit")
                if str1==str(0):
                    return self.df
                else:
                    print("Columns:")
                    print(cont)
                    str2=input("Enter the column names.Please seperate the column names with a comma ")
                    li=str2.split(",")
                    if(str1=='+'):
                        self.df[str2 + '_sum']=self.df[li].sum(axis=1)
                    elif(str1=='-'):
                        self.df[str2 + '_subtract']=self.df[li].subtract(axis=1)
                    elif(str1=='*'):
                        self.df[str2 + '_multiply']=self.df[li].prod(axis=1)
                    else:
                        self.df[str2 + '_divide']=self.df[li[1]]/self.df[li[0]]                  
                return self.df     