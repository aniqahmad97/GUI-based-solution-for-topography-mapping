# Importing Libraries 
import tkinter
from tkinter import filedialog
import matplotlib.pyplot as plt
from linecache import getline
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# initializing Main window of the GUI
window = tkinter.Tk()
# setting the geometry size
window.geometry('1600x1550')

# defining two canvas and placing them on window using place method 
canvas = tkinter.Canvas(bg='antique white')
canvas.place(x=10, y=10,height=800, width=650)

canvas1 = tkinter.Canvas(bg='grey')
canvas1.place(x=660, y=10,height=800, width=900)

# definig labels and placing them using grid method
lab0 = tkinter.Label(canvas, text='Sea Level Projections',font='Helvetica 18 bold',padx=5,pady=5,fg='#2020B2',bg='antique white')
lab0.grid(row=0,column=0)

lab1 = tkinter.Label(canvas, text='By Siyam Danishmal',font='Helvetica 9',padx=5,pady=5,fg='#ADADD8',bg='antique white')
lab1.grid(row=1,sticky='W')

def reset():
    #global plot, fig, ax
    try:
        plot1.get_tk_widget().destroy()
        plot.get_tk_widget().destroy()
        lab5.destroy()
        lab6.destroy()
        lab2.destroy()
        lab3.destroy()
        lab4.destroy()
        scale.destroy()
        but4.destroy()
        but5.destroy()
        but6.destroy()
        ent.destroy()
        
    except NameError:
        pass
    finally:
        plotmap()
        
    
# function definition for the plotting topographic map
def plotmap():
    global plot, fig, ax

    # initializing global variables to be use in other functions
     
        
    # definig figure and axis using subplot function
    fig, ax = plt.subplots(figsize=(12, 6))
    # Generating topographic map       
    cs = ax.pcolormesh(lons, lats,
                           arr_dem,
                           cmap='terrain')
    # using figurecanvastkaff to plot topographic map on canvas 
    plot = FigureCanvasTkAgg(fig, canvas1)
        
        # placement of topographic map using place method
    plot.get_tk_widget().place(relx=0.5, rely=0.5, anchor='center')
    plot.draw()
        
    # defining color bar for the topographic map
    fig.colorbar(cs)
        
    #Setting title for the topogrpahic map
    ax.set_title('Topography Map', fontsize=16)
        
# function definition for opening the file   
def openfile():
    
    # initializing global variables to be use in other functions
    global file, lons, lats, arr_dem, lab4
    
    # using askopenfilename function to open a dialog box for selecting the ascii file
    file = filedialog.askopenfilename(parent=window,
                                      initialdir=os.getcwd(),
                                      title="Please select a the asc file:",
                                      filetypes=[('asc file', '.ASC')])
    
    # reading the header of  asci file using getline function
    hdr = [getline(file, i) for i in range(1, 7)]
    
    #spliting the the header and saving the parameters
    values = [float(h.split(" ")[-1].strip()) for h in hdr]
    cols, rows, lx, ly, cell, nd = values
    res = cell

    # Load the dem into a numpy array
    arr_dem = np.loadtxt(file, skiprows=6)
    arr_dem[arr_dem <= nd] = np.nan
    
    # defining the cordinates using the columns and rows
    lons = lx + np.arange(cols)*res
    lats_r = ly + np.arange(rows)*res
    # flipping the lat up-down
    lats = lats_r[::-1]  
    
    #calling plotmap function to plot the topographic map
    plotmap()
    
    # loading the label with the file name on top of the map
    lab4 = tkinter.Label(canvas1, text=file.split('/')[-1],font='Helvetica 22 bold')
    lab4.place(x=20,y=140,width=500,height=40)

# function definition for sealevel plotting
def sealevel1():
    # initializing global variables to be use in other functions
    global plot,newheight1,value,total,lab5,lab6
    try:
        lab5.destroy()
    except NameError:
        pass
    finally:
        # getting the sealevel value from the entry 
        value = ent.get()
        
        #check if value is 0 plot orignal map
        if(value == '0'):
            plotmap()
            
            lab6 = tkinter.Label(canvas1, text='No portion of island is submerged')
            lab6.place(relx=0.05, rely=0.95)
            
        #Otherwise clear the axis and plot the value of sealevel to show submerged island
        else:
            
            newheight=arr_dem-int(ent.get())
            newheight1=np.clip(newheight,arr_dem.min(),arr_dem.max())
            value=np.sum(newheight1)
            total=np.sum(arr_dem)
            per=(value/total)*100
            #ax.clear()
            lab5 = tkinter.Label(canvas1, text='Percentage of submerged land is '+str(per))
            lab5.place(relx=0.05, rely=0.95)
            ax.contourf(lons, lats, arr_dem, [0, ent.get()], cmap='Greys')
            plot.draw()

# function definition for slide 
def slide():
    
    # initializing global variables to be use in other functions
    global sl,plot,lab5,value,total,per,lab6
    
    try:
        lab5.destroy()
        lab6 = tkinter.Label(canvas1, text='No portion of island is submerged')
        lab6.place(relx=0.05, rely=0.95)
    except:
        pass
    finally:
        # getting sealevel value from the slider function
        sl=sealevel.loc[sealevel['year'] == scale.get(), 'sealevelmm'].item()
        plot.get_tk_widget().destroy()
        plotmap()
        # if sealevel is less than 0 then plot the topographic map again
        if(sl>0):
            #plot.get_tk_widget().destroy()
            
            #plotmap()
            #Otherwise clear the axis and plot the value of sealevel to show submerged island
            newheight=arr_dem-int(scale.get())
            newheight1=np.clip(newheight,arr_dem.min(),arr_dem.max())
            value=np.sum(newheight1)
            total=np.sum(arr_dem)
            per=(value/total)*100
            #ax.clear()
            lab5 = tkinter.Label(canvas1, text='Percentage of submerged land is '+str(per))
            lab5.place(relx=0.05, rely=0.95)
    
            #else: 
            #ax.clear()
            
            #lab5.destroy()
            ax.contourf(lons, lats, arr_dem, [0, sealevel.loc[sealevel['year'] == scale.get(), 'sealevelmm'].item()], cmap='Greys')
            plot.draw()

# function definition for the topographic page
def topographicpage():
    # initializing global variables to be use in other functions
    global plot, plot1
    
    # try catch block to check if already any sealevel is loaded so to remove the label associated with it
    try:
        if (sl<0):
           lab5.destroy()
    except NameError:
            pass
        
    # run this code after executing try block
    finally:
        # destroy all the preivious widgets to plot the new widgets
        plot.get_tk_widget().destroy()
        lab2.destroy()
        lab3.destroy()
        lab4.destroy()
        scale.destroy()
        but4.destroy()
        but5.destroy()
        ent.destroy()
        
        # definig figure and axis using subplot function(for 3d contour)
        fig1, ax1 = plt.subplots(figsize=(10, 10))
        # defining the projection =3d for 3D contour plot.
        ax1 = plt.axes(projection='3d')
        #plotting the 3D contour 
        # length_of_first = len(lons)
        # lats.resize((length_of_first), refcheck=False)
        ax1.contour3D(lons, lats, arr_dem)
        
        # using figurecanvastkaff to plot topographic map on canvas 
        plot1 = FigureCanvasTkAgg(fig1, canvas1)
        # placement of topographic map using place method
        plot1.get_tk_widget().place(x=400, y=400, anchor='center')
        plot1.draw()
        
        # definig figure and axis using subplot function (for 2d contour)
        fig, ax = plt.subplots(figsize=(8, 8))
        cs = ax.contour(lons, lats,arr_dem)
        # using figurecanvastkaff to plot topographic map on canvas 
        plot = FigureCanvasTkAgg(fig, canvas)
    
        # placement of topographic map using place method
        plot.get_tk_widget().place(x=20,y=150)
        plot.draw()
        
        # setting the title for contour map
        ax.set_title('Contour Map', fontsize=16)
        # setting the contour label on 2d contour axis
        ax.clabel(cs, colors='black')

def sealevelprojectionpage():
    global plot, lab2, lab3, lab4, scale, but4, but5, but6, ent,sealevel
    try:
        plot.get_tk_widget().destroy()
        plot1.get_tk_widget().destroy()
        plotmap()
    except NameError:
        pass
    finally:
        ## Enter CSV FILE PATH HERE
        sealevel = pd.read_csv(r'C:\Users\user\Downloads\New folder (2)\Dataset 1 (2020) - provided by climate.gov.csv')
        #seavlevel.rename(columns={'mmfrom19932008average'})
        
        #generating labels and buttons and placing them using grid method on canvas
        lab2 = tkinter.Label(canvas, text='Input Data')
        lab2.grid(row=3,sticky='EW',ipadx=5,ipady=5)
        
        lab3 = tkinter.Label(canvas, text='Input Sea Level(mm)')
        lab3.grid(row=4,sticky='EW',ipadx=5,ipady=5)

        but4 = tkinter.Button(canvas, text='Choose ASCI File', command=openfile)
        but4.grid(row=3, column=1,columnspan=2,sticky='EW',ipadx=10,ipady=10)
        
        but5 = tkinter.Button(canvas, text='Load sea level', command=sealevel1)
        but5.grid(row=5, column=1,sticky='EW',ipadx=10,ipady=10)
        
        but6 = tkinter.Button(canvas1, text='Load year sea level', command=slide)
        but6.place(relx=0.05, rely=0.9)

        #generating entry on canvas for the input of sealevel value
        ent = tkinter.Entry(canvas)
        ent.grid(row=4, column=1,columnspan=2,sticky='EW',ipadx=10,ipady=10)
        
        #generating slider on the other canvas and placing it using place method 
        scale = tkinter.Scale(canvas1, from_=sealevel.min(axis=0)['year'], to=sealevel.max(axis=0)['year'], length=800, tickinterval=10, orient='horizontal')
        scale.place(relx=0.05, rely=0.8)
        
# function definition for graph page       
def graphpage():
    
    # initializing global variables to be use in other functions
    global plot, fig, ax
    
    #try and catch block to destroy all the previously loaded widgets  
    try:
        plot1.get_tk_widget().destroy()
        plot.get_tk_widget().destroy()
        lab2.destroy()
        lab3.destroy()
        lab4.destroy()
        scale.destroy()
        but4.destroy()
        but5.destroy()
        but6.destroy()
        ent.destroy()
    except NameError:
        pass
    finally:
        
        # definig figure and axis using subplot function (for sea level graph page)
        fig, ax = plt.subplots(figsize=(12, 6))
        # Using plot function to plot sealevel and year on x and y axis
        ax.plot(sealevel.year,sealevel.sealevelmm)
        #setting the title for the graph
        ax.set_title('Sea Level Rise Proejctions', fontsize=16)
        
        #setting the y label and x labels
        ax.set_ylabel('Sea Level Rise (mm)')
        ax.set_xlabel('Years')
        
        # using figurecanvastkaff to plot sealevel map on canvas 
        plot = FigureCanvasTkAgg(fig, canvas1)
        #placing the plot using place method
        plot.get_tk_widget().place(relx=0.5, rely=0.5, anchor='center')
        plot.draw()


# main buttons on the running the program are placed using grid method
but1 = tkinter.Button(canvas, text='Sea Level Projection',width=15,command=sealevelprojectionpage)
but1.grid(row=2, column=0,sticky='EW',ipady=10)

but2 = tkinter.Button(canvas, text='Topographic View',width=15, command=topographicpage)
but2.grid(row=2, column=1,sticky='EW',ipady=10)

but3 = tkinter.Button(canvas, text='Graph',width=15,command=graphpage)
but3.grid(row=2, column=2,sticky='EW',ipady=10)

but7=tkinter.Button(canvas,text='Reset',width=15,command=reset)
but7.grid(row=2,column=3,sticky='EW',ipadx=5,ipady=10)

# function to run tkinter window
window.mainloop()

