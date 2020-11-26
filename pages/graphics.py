# graphics.py contains all classes for generating graphical objects
import matplotlib.pyplot as plt, base64
from matplotlib.patches import Shadow
from PIL import Image
from abc import ABC, abstractmethod
import sys
import numpy as np
from io import BytesIO

class Graphic(ABC):

    TO_DATE_TOTALS_CASES_DECEASED = 1
    MONTHLY_TOTALS_CASES_DECEASED = 2
    PAST_30_DAYS = 3
    LOCATION_ZIPCODE = 4
    LOCATION_COUNTY = 5
    LOCATION_STATE = 6
    PIE = 7
    STACKPLOT = 8
    DUAL_PLOT = 9

    def __init__(self, *args, **kwargs):
        super().__init__()

    def __getImage(self, *args, **kwargs):
        raise NotImplementedError


class GraphicsFactory(Graphic):
    """
    This concrete class uses a simple parameterized approach to constructing the required graphics subclass
    objects needed by the consumer.
    """
    def __init__(self, *args, **kwargs):
        self.__createGraphicInstance(*args, **kwargs)

    def __getImage(self, *args, **kwargs):
        pass

    def __isImageCreated(self, image):
        """
        docstring
        """
        try:
            if self.image != None:
                return True                    
            else:
                return False
        except:
            print ("GraphicsFactory.__isImageCreated() - unexpected error: ",sys.exc_info()[0])
            return False    

    def __createGraphicInstance(self, *args, **kwargs):
        """
        Use the args to identify and instantiate a class that can generate the requested graphic
        """
        try:
            if 'GRAPHIC_TYPE' in kwargs:
                if kwargs['GRAPHIC_TYPE'] == Graphic.PIE:
                    graphInstance = PieGraph()                   
                    self.image = graphInstance.getImage(*args,**kwargs)
                    self.ImageAvailable=self.__isImageCreated(self.image)
                    return 

                if kwargs['GRAPHIC_TYPE'] == Graphic.STACKPLOT:
                    graphInstance = StackPlotGraph()                   
                    self.image = graphInstance.getImage(*args,**kwargs)
                    self.ImageAvailable=self.__isImageCreated(self.image)
                    return                    

                if kwargs['GRAPHIC_TYPE'] == Graphic.DUAL_PLOT:
                    graphInstance = DualPlotGraph()                   
                    self.image = graphInstance.getImage(*args,**kwargs)
                    self.ImageAvailable=self.__isImageCreated(self.image)
                    return 

            print ("CovidMessages.__createCovidModelInstance() - did not receive a recognizable model type - no model object instantiated. Args received = ",kwargs)
            return None
        except:
            print ("CovidMessages.__createCovidModelInstance() - unexpected error: ",sys.exc_info()[0])
            return None


class PieGraph(Graphic):
    __sql = ''
    __data = None

    def __init__(self, *args, **kwargs):
        super().__init__()

    def getImage(self, *args, **kwargs):
        """
        docstring
        """
        print("PieGraph.getImage()  kwargs=", kwargs)
        if 'IMAGE_DATA' not in kwargs:
            return None

        return self.__constructImage(self, *args, **kwargs)
   
    def __constructImage(self, *args, **kwargs):
        """
        docstring
        """
        try:
            labels = 'Cases', 'Deceased'

            request_data = kwargs['IMAGE_DATA']
            #  case = 100*(Cases-Deceased)/Cases

            case = 100*(int(request_data[0]['Cases'])-int(request_data[0]['Deceased']))/int(request_data[0]['Cases'])
            
            #  deceased = 100*(Deceased/Cases)
            deceased = 100*(int(request_data[0]['Deceased'])/int(request_data[0]['Cases']))
            sizes = [case, deceased]
            explode = (0, 0.1)

            plt.ioff()
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax1.legend(loc='upper left',fancybox=True)
            ax1.set_title(str(request_data[0]['County']) + " County, " + str(request_data[0]['State']) + " - Ratio of Confirmed to Deceased")

            # save and return
            buf = BytesIO()
            plt.savefig(buf, transparent = True, format="png")
            buf_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            return buf_base64

        except:
            print ("PieGraph.__constructImage() - unexpected error: ",sys.exc_info()[0])
            return None


class StackPlotGraph(Graphic):
    __sql = ''
    __data = None

    def __init__(self, *args, **kwargs):
        super().__init__()

    def getImage(self, *args, **kwargs):
        """
        docstring
        """
        print("StackPlotGraph.getImage()  kwargs=", kwargs)
        if 'IMAGE_DATA' not in kwargs:
            return None

        return self.__constructImage(self, *args, **kwargs)
   
    def __constructImage(self, *args, **kwargs):
        """
        docstring
        """
        try:
            request_data = kwargs['IMAGE_DATA']

            months = [d['Month_part'] for d in request_data if 'Month_part' in d]
            # remove dupe month names from list
            months = list(dict.fromkeys(months))
            
            # get unique set of FIPS - will be used to filter data for each graph
            FIPS = [d['FIPS'] for d in request_data if 'FIPS' in d]
            # reduce list of FIPS values to unique set (becomes a dictionary)
            FIPS=list(dict.fromkeys(FIPS))
            
            # start new row list that will contain only the FIPS to be graphed - this currently constrains to the first FIPS found, and
            # msg text will be provided explaining to the user that they need to search additional counties within the state for more information
            row_list=list()
            for item in request_data:
                if item['FIPS'] == FIPS[0]:
                    row_list.append(item)
            cases = [d['Cases'] for d in row_list if 'Cases' in d]
            deceased = [d['Deceased'] for d in row_list if 'Deceased' in d]

            # get unique name of county - will be used in display literals
            county = [d['county'] for d in row_list if 'county' in d]
            # reduce list of FIPS values to unique set (becomes a dictionary)
            county=set(county)
            # convert the dictionary back to a list structure
            county=list(county)

            # get unique name of state - will be used in display literals
            state = [d['state'] for d in row_list if 'state' in d]
            # reduce list of FIPS values to unique set (becomes a dictionary)
            state=set(state)
            # convert the dictionary back to a list structure
            state=list(state)

            population = {
                'Cases': cases,
                'Deceased': deceased,
            }
            plt.ioff()
            fig, ax = plt.subplots()
            ax.stackplot(months, population.values(),
                        labels=population.keys())
            ax.legend(loc='upper left',fancybox=True)
            ax.set_title(county[0] + ' County, '+ state[0] + ' - FIPS ' + FIPS[0] + ' - Monthly Growth')
            ax.set_xlabel('Month')
            ax.set_ylabel('Population Affected')
            ax.facecolor = 'inherit'

            # save and return
            buf = BytesIO()
            plt.savefig(buf, transparent=True, format="png")
            buf_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            return buf_base64

        except:
            print ("StackPlotGraph.__constructImage() - unexpected error: ",sys.exc_info()[0])
            return None

class DualPlotGraph(Graphic):
    __sql = ''
    __data = None

    def __init__(self, *args, **kwargs):
        super().__init__()

    def getImage(self, *args, **kwargs):
        """
        docstring
        """
        # print("DualPlotGraph.getImage()  kwargs=", kwargs)
        # if 'COUNTY_DATA' not in kwargs or 'STATE_DATA' not in kwargs:
        #     return None

        return self.__constructImage(self, *args, **kwargs)
   
    def __constructImage(self, *args, **kwargs):
        """
        docstring
        """
        try:
            if 'COUNTY_DATA' in kwargs:
                county_data = kwargs['COUNTY_DATA']
            else:
                print("DualPlotGraph.__constructImage() - no county data provided - exiting early")
                return None

            if 'STATE_DATA' in kwargs:
                state_data = kwargs['STATE_DATA']
            else:
                print("DualPlotGraph.__constructImage() - no state data provided - exiting early")
                return None

            if 'STATE' in kwargs:
                state_name = kwargs['STATE']
            else:
                print("DualPlotGraph.__constructImage() - no state name provided - exiting early")
                return None

            dates = [d['event_day'] for d in county_data if 'event_day' in d]
            # remove dupe dates from list
            dates = list(dict.fromkeys(dates))
            # days 
            days = len(dates)

            # get unique set of FIPS - will be used to filter data for each graph
            FIPS = [d['FIPS'] for d in county_data if 'FIPS' in d]
            # reduce list of FIPS values to unique set (becomes a dictionary)
            FIPS=list(dict.fromkeys(FIPS))
            
            # start new row list that will contain only the FIPS to be graphed - this currently constrains to the first FIPS found, and
            # msg text will be provided explaining to the user that they need to search additional counties within the state for more information
            row_list=list()
            for item in county_data:
                if item['FIPS'] == FIPS[0]:
                    row_list.append(item)
            county_cases = [d['Cases'] for d in row_list if 'Cases' in d]
            county_cases_min=min(county_cases)
            county_cases_max=max(county_cases)
            county_deceased = [d['Deceased'] for d in row_list if 'Deceased' in d]
            county_deceased_min=min(county_deceased)
            county_deceased_max=max(county_deceased)
        
            # get unique name of county - will be used in display literals
            county = [d['county'] for d in row_list if 'county' in d]
            # reduce list of FIPS values to unique set (becomes a dictionary)
            county=set(county)
            # convert the dictionary back to a list structure
            county=list(county)

            # begin adjacent subplots image
            t = np.arange(0, days, 1)

            # state data
            state_cases = [d['Cases'] for d in state_data if 'Cases' in d]
            state_cases_min=min(state_cases)
            state_cases_max=max(state_cases)
            state_deceased = [d['Deceased'] for d in state_data if 'Deceased' in d]
            state_deceased_min=min(state_deceased)
            state_deceased_max=max(state_deceased)
            
            # --cases graphs--
            plt.ioff()	
            fig_cases, axs_cases = plt.subplots(2, 1, sharex=True)
            # Remove horizontal space between axes
            fig_cases.subplots_adjust(hspace=0)

            # Plot each graph, and manually set the y tick values
            axs_cases[0].plot(t, county_cases)
            axs_cases[0].set_yticks(np.arange(county_cases_min, county_cases_max, ((county_cases_max-county_cases_min)//10)))
            axs_cases[0].set_ylim(county_cases_min, county_cases_max*1.1)

            axs_cases[1].plot(t, state_cases)
            axs_cases[1].set_yticks(np.arange(state_cases_min, state_cases_max, (state_cases_max-state_cases_min)//10))
            axs_cases[1].set_ylim(state_cases_min, state_cases_max*1.1)

            label=county[0]+' County'
            axs_cases[0].set_ylabel(label)
            label= 'Past '+ str(days) +' Days'
            axs_cases[1].set_xlabel(label)
            label=str(state_name)
            axs_cases[1].set_ylabel(label)
            axs_cases[0].legend(loc='upper left',fancybox=True)
            axs_cases[0].set_title(county[0] + ' County vs. '+ str(state_name) + ' - Daily New Cases')
            buf = BytesIO()
            plt.savefig(buf, transparent=True, format="png")
            cases_graph = "data:image/png;base64,"
            cases_graph += base64.b64encode(buf.getvalue()).decode('utf-8')

            #--- deceased graphs ---
            fig_deceased, axs_deceased = plt.subplots(2, 1, sharex=True)
            # Remove horizontal space between axes
            plt.ioff()
            fig_deceased.subplots_adjust(hspace=0)

            # Plot each graph, and manually set the y tick values
            axs_deceased[0].plot(t, county_deceased)
            if (county_deceased_max-county_deceased_min)<10:
                    ticks=.5
            else:
                    ticks=1
            axs_deceased[0].set_yticks(np.arange(county_deceased_min, county_deceased_max, ((county_deceased_max-county_deceased_min)//ticks)))
            axs_deceased[0].set_ylim(county_deceased_min, county_deceased_max*1.1)

            axs_deceased[1].plot(t, state_deceased)
            axs_deceased[1].set_yticks(np.arange(state_deceased_min, state_deceased_max, (state_deceased_max-state_deceased_min)//10))
            axs_deceased[1].set_ylim(state_deceased_min, state_deceased_max*1.1)

            label=county[0]+' County'
            axs_deceased[0].set_ylabel(label)
            label= 'Past '+ str(days) +' Days'
            axs_deceased[1].set_xlabel(label)
            label=str(state_name)
            axs_deceased[1].set_ylabel(label)
            axs_deceased[0].legend(loc='upper left',fancybox=True)
            axs_deceased[0].set_title(county[0] + ' County vs. '+ str(state_name) + ' - Daily Deceased')
            buf = BytesIO()
            plt.savefig(buf, transparent=True, format="png")
            deceased_graph = "data:image/png;base64,"
            deceased_graph += base64.b64encode(buf.getvalue()).decode('utf-8')
            return cases_graph,deceased_graph

        except:
            print ("DualPlotGraph.__constructImage() - unexpected error: ",sys.exc_info()[0])
            return None