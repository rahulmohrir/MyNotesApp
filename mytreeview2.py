import kivy
kivy.require('2.3.1')
import os
from kivy.app import App
import PIL
from PIL import Image as PILImage
from PIL import ImageOps
import shutil
import webbrowser
from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivy.uix.layout import Layout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.treeview import TreeView, TreeViewLabel, TreeViewNode
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.modalview import ModalView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem, TabbedPanelStrip, StripLayout, TabbedPanelHeader
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooser, FileChooserListView, FileChooserListLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.storage.jsonstore import JsonStore
import json
from collections import defaultdict
from kivy.clock import Clock
from functools import partial
from kivy.event import EventDispatcher
from kivy.core.window import Window

from kivy.core.clipboard import Clipboard
from kivy.lang import Builder



class TreeViewScreen(Screen):
    hovered_tree = BooleanProperty(False)
    def __init__(self, **kw):
        super(TreeViewScreen, self).__init__(**kw)
        self.info_popup = MyInfoPopup()
    ## On enter bind the window to open the first info popup
    def on_enter(self, *args):
        print('Treebind')
        Window.bind(mouse_pos = self.on_mouse_pos)
        return super().on_enter(*args)
    ## on leave unbind the window    
    def on_leave(self, *args):
        print('Treeunbind')
        Window.unbind(mouse_pos = self.on_mouse_pos)
        return super().on_leave(*args)
        
    
    def on_mouse_pos(self, window, pos):
        ## On mouse position check if popup is open 
        for widget in App.get_running_app().root_window.children:
           
            if isinstance(widget, Popup):
               
                return True
            
               
       
        
        if self.collide_point(*pos):
         # 1. Convert window/screen coordinates to this widget's local coordinates
            local_pos = self.to_widget(*pos)
   
           ## Get node at the position and check if it is the root
            node = self.tree.get_node_at_pos(local_pos)
        
            # Check if the mouse position collides with the widget`s root node
    
            if node == self.tree.root:
                if not self.hovered_tree:
                    self.hovered_tree = True
            
                    self.add_first_info_label()
                    self.hover_timer = Clock.schedule_once(self.dismiss_first_info_popup, 3.0)
            else:
                if self.hovered_tree:
                    self.hovered_tree = False
                    self.remove_first_info_label()
    ## Function to open the first info popup
    def add_first_info_label(self):
        
        
        self.info_popup.open()
     ## Function to closethe first info popup
    def remove_first_info_label(self):
        self.info_popup.dismiss()
    def dismiss_first_info_popup(self, dt):
        self.info_popup.dismiss()

    pass

class MyTree(TreeView):

    pass
class TreeViewLabel(TreeViewLabel):
    pass

class MyInfoPopup(Popup):
    pass

class MyTreeViewLabel(TreeViewLabel):
 
    pass
 
    
class MyClickableLabel(Label, TreeViewNode):

    pass
class MyTextInputNode(TextInput):
    pass
class MyTouchableLabel(ButtonBehavior,Label):
    # Default text color
    normal_color = ListProperty([1, 1, 1, 1]) 
    # Highlighted text color
    hover_color = ListProperty([.52, 0.80, .92, 1 ])  

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Bind the mouse movement to our hover function
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, window, pos):
        # Compensate for any relative layout coordinates
        inside = self.collide_point(*self.to_widget(*pos))
        
        if inside:
            self.color = self.hover_color
        else:
            self.color = self.normal_color
    pass
class MyLabel(Label):
    pass
class MyButton(Button):
    pass
class MyFirstPopupWithAdd(Popup):
    pass
class MyFirstPopup(Popup):
    pass

class MyEditedNodePopup(Popup):
    pass
class MyAddNodePopup(Popup):
    pass
class MyDeleteNodePopup(Popup):
    pass
class MyRootDeleteNodePopup(Popup):
    pass
    
class TabScreen(Screen):
    
    pass
class MyTabTextInput(TextInput):
    txt_inpt = ObjectProperty(None)
    max_lines = NumericProperty(8)
    
    def __init__(self, **kwargs):
        super(MyTabTextInput, self).__init__(**kwargs)
        self.insert_line_popup = MyInsertLineInfoPopup()

    def on_touch_down(self, touch):
        # Let the TextInput handle its own focus/cursor logic first
        res = super().on_touch_down(touch)
        
        # Check if the touch happened inside this widget
        if self.collide_point(*touch.pos):
            # Return False to force Kivy to pass the touch to widgets underneath
           
            return False
        return res
    
    def insert_text(self, substring, from_undo=False):
        
        ## Gives number of lines currently displayed
        line_count = len(self._lines)
        ## Split the substring by punctuation mark 
        substring_lines = substring.split('.')
        ## Count the number of lines in the substring
        substring_count = len(substring_lines)
        
       ## If the displayed lines and lines in the substring is more than the maximum lines insert nothing and show a info label
        if  line_count + substring_count> self.max_lines :
           
            substring = ""
            self.open_insert_line_popup()
        else:
            substring = substring
    
        
        Clock.schedule_once(self.move_cursor, 0)
       
        return super(MyTabTextInput, self).insert_text(substring, from_undo=from_undo)   
    
    def move_cursor(self, dt):
        ##self.do_cursor_movement('cursor_end')
        print(len(self._lines) - 1)
        print(len(self._lines[len(self._lines) - 1]))

        self.cursor = (len(self._lines[len(self._lines) - 1]), len(self._lines) - 1)

    def do_backspace(self, from_undo=False, mode='bkspc'):
        # First, perform the standard backspace (removes char)

        Clock.schedule_once(self.move_cursor_back, 0)
        super().do_backspace(from_undo=from_undo, mode=mode)
    
    
    def move_cursor_back(self, dt):
        self.cursor = (len(self._lines[len(self._lines) - 1]), len(self._lines) - 1)

    
    
    
    def open_insert_line_popup(self):
        self.insert_line_popup.open()
        Clock.schedule_once(self.autodismiss_insert_line_popup, 3)
    def autodismiss_insert_line_popup(self, dt):
        self.insert_line_popup.dismiss()
    pass
class MyInsertLineInfoPopup(Popup):
    
       
    pass
class MyTabbedPanelStrip(TabbedPanelStrip):
    pass
class StripLayout(StripLayout):
    pass
class MyTabbedPanelItem(TabbedPanelItem):
    pass
class MyTabbedPanelHeader(TabbedPanelHeader):
    pass
class MyTabMainBoxLayout(BoxLayout):
    pass
class MyLowerTabBoxLayout(BoxLayout):
    pass
class MyTabbedPanel(TabbedPanel):
   
    pass
class MyTabButton(Button):
    pass
class MyTabTouchableLabel(Label, ButtonBehavior):
     # Default text color
    normal_color = ListProperty([1, 1, 1, 1]) 
    # Highlighted text color
    hover_color = ListProperty([.52, 0.80, .92, 1 ])  

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Bind the mouse movement to our hover function
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, window, pos):
        # Compensate for any relative layout coordinates
        inside = self.collide_point(*self.to_widget(*pos))
        
        if inside:
            self.color = self.hover_color
        else:
            self.color = self.normal_color
    pass
class MyTabLabel(Label):
    
    pass

class MyFileChooser(FileChooser):
    pass

class MyFCPopup(Popup):
    pass

class MyImagePopup(Popup):
    image_path= ObjectProperty(None)
    pass

class Image(Image):
    pass

class MyFileRenamePopup(Popup):
    pass

class MyImageDisplayPopup(Popup):
    pass



class MyPackLabel(Label):
    pass


class RootWidget(ScreenManager):
    text = StringProperty('')
    
    level = NumericProperty()
    nodes = ListProperty()
    source = StringProperty(None)
    my_tab_label = ObjectProperty(None)
   
    selected_node = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
    
        ## First Screen with tree structure
        self.treescreen = TreeViewScreen(name = 'treescreen')

        ## Second Screen with tabs
        self.tabscreen = TabScreen(name = 'tabscreen')

        ## Add tree structure to screen
        self.treescreen.tree = MyTree()

        self.treescreen.treeviewlabel = MyTreeViewLabel()
        self.treescreen.tree.myclickablelabel = MyClickableLabel()

        
        ## First popup with add, edit, delete options
        
        self.treescreen.myfirstpopup = MyFirstPopup()

        ## Second popup with editable input to change label of node
        self.treescreen.myeditednodepopup = MyEditedNodePopup()

        ## Second popup to add a node
        self.treescreen.myaddnodepopup = MyAddNodePopup()

        ## Second popup to delete a node
        self.treescreen.mydeletnodepopup = MyDeleteNodePopup()

        self.treescreen.myrootdeletenodepopup = MyRootDeleteNodePopup()
        self.tabscreen.panel=  MyTabbedPanel()
        self.mylowertabboxlyout = MyLowerTabBoxLayout()
        self.tab_text_input = MyTabTextInput()
        self.tabscreen.panel.my_tab_label = MyTabLabel()
        
       
        ## Limiting the level and number of nodes added at each level
        
        self.max_nodes = 3
        
        self.topic_dict = {}

        ## Get the app running status
        self.app = App.get_running_app()

        ## Select a node by the touch down event
        self.selected_node = self.treescreen.tree.selected_node

        self.tabscreen.my_fc_popup = MyFCPopup()
        self.tabscreen.my_image_popup = MyImagePopup()
        self.my_image = self.tabscreen.my_image_popup.ids.display_image
        self.tabscreen.my_file_chooser = MyFileChooser()
        self.tabscreen.fc_list_view = FileChooserListView()
        self.tabscreen.my_file_rename_popup = MyFileRenamePopup()
        self.tabscreen.my_image_display_popup = MyImageDisplayPopup()
        self.my_display_image = self.tabscreen.my_image_display_popup.ids.display_image_only
        
        
        

        self.add_widget(self.treescreen)
        self.treescreen.add_widget(self.treescreen.tree)
        self.add_widget(self.tabscreen)
        self.tabscreen.add_widget(self.tabscreen.panel)
    

        

    ## Function to open the first popup with add, edit, delete options

    def first_popup_open(self):
        self.selected_node = self.treescreen.tree.selected_node
        self.treescreen.myfirstpopup.open()

    ## Function to open the add node popup
    def open_add_node_popup(self):
        self.treescreen.myfirstpopup.dismiss()
        self.treescreen.myaddnodepopup.open()

    ## Function to add node at a desired level
    def add_node_level(self):
        
       
        self.node_number = len(self.selected_node.nodes)
        ## Selected node by the touch down event
        
        
        ## Compare the node number with maximum node allowed
        if self.node_number < self.max_nodes and self.selected_node.level == 0 :
            
            self.add_level_1()
      
        elif self.node_number < self.max_nodes and self.selected_node.level == 1:
           
            self.add_level_2()
            
               
        elif self.node_number < self.max_nodes and self.selected_node.level == 2:
           
            self.add_level_3()
                
        
        else:
           
            self.treescreen.tree.deselect_node(self.selected_node)
              
        
        
        
        
   ## function to add the first level
    def add_level_1(self):

        sub_dict = {}

        ## Get the node text entered by user to create a json file
        subject_key = self.treescreen.myaddnodepopup.ids.input.text
       
        file_name = f"{subject_key}.json"
        file_store = [file_name]
        for file_name in file_store:

            path = self.app.user_data_dir
            file_path = os.path.join(path, file_name)
       
            with open(file_path, 'w') as file_object:
                
               sub_dict[ subject_key] = {}
               json_data = json.dump(sub_dict, file_object, indent= 4)

        ## Add node at level 1 with node_key property which will remain fixed even the node lebel changes
        level_1_node = self.treescreen.tree.add_node(MyTreeViewLabel(text = subject_key, node_key = subject_key))
        
        self.treescreen.myaddnodepopup.dismiss()  
        
    ## function to add second level        
    def add_level_2(self):

        ## Get the name of second level node
        topic_key = self.treescreen.myaddnodepopup.ids.input.text
        
        topic_dict = {}
        
        new_json_data = defaultdict(dict)
        
        subject_key = self.selected_node.node_key
        
        file_name = f"{subject_key}.json"
        path = self.app.user_data_dir
        file_path = os.path.join(path, file_name)
        with open(file_path, 'r') as file_object:

            json_data= json.load(file_object)

        ## access the subject key value
            value = json_data[subject_key]
           

        ## Assign value to dictionary    
            topic_dict = value
           
        ## Update the dictionary   
        topic_dict.update({topic_key: {}})
       
           
        new_json_data[subject_key] = topic_dict
        with open(file_path, 'w') as file_object:
            
            
            topic_string = json.dump(new_json_data, file_object, indent= 4)

           
        level_2_node = self.treescreen.tree.add_node(MyTreeViewLabel(text = topic_key, node_key = topic_key ), self.selected_node)   
        
        self.treescreen.myaddnodepopup.dismiss() 
                    
     ## function to add third level
    def add_level_3(self):
        
        heading_dict = {}
        
        new_json_data_sub = {}
        ## Get the level two node
        level_2_node = self.selected_node

        ## Get the level 1 node by accessing its parent
        level_1_node = level_2_node.parent_node

        subject_key = level_1_node.node_key
        topic_key = level_2_node.node_key
        heading_key = self.treescreen.myaddnodepopup.ids.input.text
        
        
        file_name = f"{subject_key}.json"
        path = self.app.user_data_dir
        file_path = os.path.join(path, file_name)
        with open(file_path, 'r') as file_object:
        
                
            json_data= json.load(file_object)

        ## access the subject key value
            value = json_data[subject_key]
            
            heading_dict = value[topic_key]
            
            
            heading_dict.update({heading_key :{'PG1' : '', 'PG2' : '', 'PG3' : '', 'PG4' : '', 'PG5' : ''}})
        
            value[topic_key]= heading_dict
            new_json_data_sub[subject_key] = value
        
        with open(file_path, 'w') as file_object:
            
            
            topic_string = json.dump(new_json_data_sub, file_object, indent= 4)
                
        level_3_node = self.treescreen.tree.add_node(MyClickableLabel(text = heading_key, node_key = heading_key ), self.selected_node)            
        self.treescreen.myaddnodepopup.dismiss()   

    ## Function to load the data when clicked on the label
    def load_data_when_clicked(self):
        
        self.selected_node = self.treescreen.tree.selected_node
        level_3_node = self.selected_node
        
        level_2_node = self.selected_node.parent_node
        level_1_node = level_2_node.parent_node
               
        heading_key = level_3_node.node_key
           
        topic_key = level_2_node.node_key

        subject_key = level_1_node.node_key
        file_name =  f"{subject_key}.json"
        
        path = self.app.user_data_dir
        file_path = os.path.join(path, file_name)
       
        with open(file_path, 'r') as file_object:
                
           
            json_data = json.load(file_object)
           
            heading_key_data = json_data[subject_key][topic_key][heading_key]
            
            
            ##self.tabscreen.panel.ids.textinput1.readonly = True
            self.tabscreen.panel.ids.textinput2.readonly = True
            self.tabscreen.panel.ids.textinput3.readonly = True
            self.tabscreen.panel.ids.textinput4.readonly = True
            self.tabscreen.panel.ids.textinput5.readonly = True
            a = heading_key_data['PG1']
            self.tabscreen.panel.ids.textinput1.insert_text(a)
            print(a)

            ##self.tabscreen.panel.ids.textinput1.text = heading_key_data['PG1']
            self.tabscreen.panel.ids.textinput2.text = heading_key_data['PG2'] 
            self.tabscreen.panel.ids.textinput3.text = heading_key_data['PG3']
            self.tabscreen.panel.ids.textinput4.text = heading_key_data['PG4']
            self.tabscreen.panel.ids.textinput5.text = heading_key_data['PG5']

            return file_object, subject_key, topic_key
        
    def save_data_after_editing(self, instance):
        ## If the button is edit then set readonly property to false 
        if instance.text == 'Edit':

            instance.text = 'Save'
            self.tabscreen.panel.ids.textinput1.readonly = False
            self.tabscreen.panel.ids.textinput2.readonly = False
            self.tabscreen.panel.ids.textinput3.readonly = False
            self.tabscreen.panel.ids.textinput4.readonly = False
            self.tabscreen.panel.ids.textinput5.readonly = False
           
        else:

        ## Else call the edit event 2 function 
            self.edit_event_2()
           
            instance.text = 'Edit'
            self.tabscreen.panel.ids.textinput1.readonly = True
            self.tabscreen.panel.ids.textinput2.readonly = True
            self.tabscreen.panel.ids.textinput3.readonly = True
            self.tabscreen.panel.ids.textinput4.readonly = True
            self.tabscreen.panel.ids.textinput5.readonly = True
    

    ## Function to save data after editing is complete    
    
    def edit_event_2(self):
        level_3_node = self.selected_node
        
        level_2_node = level_3_node.parent_node
        level_1_node = level_2_node.parent_node
              
        subject_key = level_1_node.node_key
        topic_key = level_2_node.node_key
        heading_key = self.selected_node.node_key
        file_name =  f"{subject_key}.json"
        path = self.app.user_data_dir
        file_path = os.path.join(path, file_name)
        
        
        text_pg1 = self.tabscreen.panel.ids.textinput1.text
        text_pg2 = self.tabscreen.panel.ids.textinput2.text
        text_pg3 = self.tabscreen.panel.ids.textinput3.text
        text_pg4 = self.tabscreen.panel.ids.textinput4.text
        text_pg5= self.tabscreen.panel.ids.textinput5.text
        page_dict = {'PG1' : f"{text_pg1}", 'PG2' : f"{text_pg2}", 'PG3' : f"{text_pg3}", 'PG4' : f"{text_pg4}", 'PG5' : f"{text_pg5}" }
        print(text_pg1)
        with open(file_path, 'r') as file_object:
            data_loaded = json.load(file_object)
            
        with open(file_path, 'w') as file_object:
           
            data_loaded[subject_key][topic_key][heading_key] = page_dict
            
            
            json.dump(data_loaded, file_object, indent= 4)
    ## Function to read data after user click the read button.
    
    def read_data_back(self):
       
        level_3_node = self.selected_node
        
        level_2_node = level_3_node.parent_node
        level_1_node = level_2_node.parent_node
              
        subject_key = level_1_node.node_key
        topic_key = level_2_node.node_key
        heading_key = self.selected_node.node_key
        file_name =  f"{subject_key}.json"
        path = self.app.user_data_dir
        file_path = os.path.join(path, file_name)
        
        
        text_pg1 = self.tabscreen.panel.ids.mylabel_1.text
        text_pg2 = self.tabscreen.panel.ids.mylabel_2.text
        text_pg3 = self.tabscreen.panel.ids.mylabel_3.text
        text_pg4 = self.tabscreen.panel.ids.mylabel_4.text
        text_pg5= self.tabscreen.panel.ids.mylabel_5.text
        page_dict = {'PG1' : f"{text_pg1}", 'PG2' : f"{text_pg2}", 'PG3' : f"{text_pg3}", 'PG4' : f"{text_pg4}", 'PG5' : f"{text_pg5}" }
        
        with open(file_path, 'r') as file_object:
            data_loaded = json.load(file_object)
            data_loaded[subject_key][topic_key][heading_key] = page_dict
            
        ##with open(file_path, 'w') as file_object:
           
            ##data_loaded[subject_key][topic_key][heading_key] = page_dict
            
            
            ##json.dump(data_loaded, file_object, indent= 4)
    
    ## Function to open the edit popup after clicking the edit button
    def open_edit_node_popup(self):
        self.treescreen.myfirstpopup.dismiss()
        
        self.treescreen.myeditednodepopup.open()
        selected_node = self.treescreen.tree.selected_node
        edited_node_label = selected_node.text  
        self.treescreen.myeditednodepopup.ids.input.text = edited_node_label



    ## Function to edit Node Label
    def edit_node_label(self):
        
        new_node_label = self.treescreen.myeditednodepopup.ids.input.text
        if new_node_label != '':
            
            if self.treescreen.tree.selected_node:
                self.treescreen.tree.selected_node.text = new_node_label
            else:
                print('No Node Selected')
        self.treescreen.myeditednodepopup.dismiss()
        return new_node_label
    
    def cancel_myadd_node_popup(self):
        self.treescreen.myaddnodepopup.dismiss()

    ## Function to cancel the Second Popup
    def cancel_edited_node_popup(self):
        self.treescreen.myeditednodepopup.dismiss()

    def open_delete_node_popup(self):
        self.treescreen.myfirstpopup.dismiss()
        self.treescreen.mydeletnodepopup.open()

    def cancel_delete_node_popup(self):
        self.treescreen.mydeletnodepopup.dismiss()

    ## Function to delete the Selected Node
    def delete_node(self):
        
        selected_node = self.treescreen.tree.selected_node
        if selected_node.level == 1:
            subject_key = self.selected_node.node_key
            file_name = f"{subject_key}.json"
            
        
        ## Get the running app status to access the user data directory
            
            path = self.app.user_data_dir
            file_path = os.path.join(path, file_name)
            os.remove(file_path)
            print('ALl nodes below will be deleted')
            self.treescreen.tree.remove_node(self.treescreen.tree.selected_node)

       
        elif selected_node.level == 2:
            print('ALl nodes below will be deleted')
            self.treescreen.tree.remove_node(self.treescreen.tree.selected_node)
            

        elif selected_node.level == 3:
            print('All nodes below will be deleted')
            self.treescreen.tree.remove_node(self.treescreen.tree.selected_node)
        else:
            self.root_delete_popup_open()
            print('No Node Selected')
       
        self.treescreen.mydeletnodepopup.dismiss()

    def root_delete_popup_open(self):
        self.treescreen.myrootdeletenodepopup.open()

    def root_delete_popup_cancel(self):
        self.treescreen.myrootdeletenodepopup.dismiss()
    
    ## Function to toggle the tabbedpanel header
    def toggle_header(self):

         # Access the tab strip layout directly
        if self.tabscreen.panel._tab_layout.height > 0:
            self.tabscreen.panel._tab_layout.height = 0
            self.tabscreen.panel._tab_layout.opacity = 0
            # Optional: disable further touches to the header
            self.tabscreen.panel._tab_layout.disabled = True 
            

        else:
            self.tabscreen.panel._tab_layout.height = 100 
            self.tabscreen.panel._tab_layout.opacity = 1
            self.tabscreen.panel._tab_layout.disabled = False
    ## Function to toggle the tabbedpanel lower boxlayout
    def   toggle_lower_box(self, lowertabid):
        self.tabscreen.panel.ids.mylowertabbox = lowertabid
        if self.tabscreen.panel.ids.mylowertabbox.height > 0:
            print(self.tabscreen.panel.ids.mylowertabbox.height)  
            
            self.tabscreen.panel.ids.mylowertabbox.height = 0
            self.tabscreen.panel.ids.mylowertabbox.size_hint_y = None
            self.tabscreen.panel.ids.mylowertabbox.opacity = 0
            self.tabscreen.panel.ids.mylowertabbox.disabled = True
        else:
            print(self.tabscreen.panel.ids.mylowertabbox.height)
            self.tabscreen.panel.ids.mylowertabbox.height = 75
            
            self.tabscreen.panel.ids.mylowertabbox.opacity = 1
            self.tabscreen.panel.ids.mylowertabbox.disabled = False

    def on_enter(self):
       
        self.tabscreen.panel.ids.tab1.focus = True

    ## Function to open the filechooser popup
    def fc_popup(self, textinput):
        self.txt_inpt = textinput
        
        self.tabscreen.my_fc_popup.open()

     ## Function to select a file from the file chooser   
    def file_selected(self, selection):
        if selection:
        # selection is a list of full file paths
            print(f"User selected: {selection[0]}")

            
    def image_display(self,filechooser,selection):
       
        if selection:
        # selection is a list of full file paths
           
            self.image_path = selection[0]  # Selection is a list of absolute paths
            if os.path.isdir(self.image_path):
                print(f"'{self.image_path}' is a folder.")

            else:
               
                self.tabscreen.my_fc_popup.dismiss()
                self.tabscreen.my_image_popup.open()
                self.image_path = selection[0]
                self.get_fixed_image(self.image_path)

    ## Function to get the image and handle its orientation
    def get_fixed_image(self, path):
        img = PILImage.open(path)
        # Automatically handles orientation based on EXIF
        img = ImageOps.exif_transpose(img) 
        img.save(path)
        self.open_file_rename_popup(path)
        self.my_image.source = path
        
        return path

    def cancel_my_image_popup(self):
        self.tabscreen.my_image_popup.dismiss()

    
    def open_file_rename_popup(self, path):
        print(path)
        self.tabscreen.my_image_popup.dismiss()
        self.tabscreen.my_file_rename_popup.open()

     ## Function to rename the file   
    def rename_file(self):

        old_path = self.image_path
       
       
            # Get the directory and the original file extension
        directory = os.path.dirname(old_path)

        extension = os.path.splitext(old_path)[1]
            
            # Create the new full path
        new_name = self.tabscreen.my_file_rename_popup.ids.file_text_rename.text.strip()
        
        
        data_dir = self.app.user_data_dir
        if new_name:
            
            new_path = os.path.join(data_dir , new_name + extension)
           
            
            try:
                shutil.copy2(old_path, new_path)
                
                # Optional: Refresh the filechooser to show the change
                ##self.ids.filechooser._update_files() 
            except Exception as e:
                print(f"Error: {e}")
        self.add_image_link( new_path, new_name)
        self.tabscreen.my_file_rename_popup.dismiss()

     ## Function to add image link to the textinput   
    def add_image_link(self, path, name):
        
       
        markup_link = f"Click [ref= {path}][color=0000ff][u]here[/u][/color][/ref] to open the image."
        
        self.txt_inpt.readonly = False
        displayed_markup = f" Fig. -{name}.  {markup_link}"
        self.txt_inpt.insert_text( f"\n {displayed_markup} ")

    ## Function to open the link    
    def open_link(self, instance, ref_value):
        self.tabscreen.my_image_display_popup.open()
       
        Clock.schedule_once(partial(self.display_image,ref_value), 1)

    ## Function to display the image after clicking the markup
    def display_image(self,ref_value,dt):
        new_name = ref_value.strip()
        data_dir = self.app.user_data_dir
        absolute_path = os.path.join(data_dir, new_name)
       
        ##self.my_display_image.source = ref_value
        if os.path.exists(absolute_path):
            self.my_display_image.source = absolute_path
            self.my_display_image.reload()
            return 
        
        else:
            print(f"Error: {absolute_path} does not exist!")

class MyTreeviewApp2(App):
    
    def build(self):

        ## Json File for Storing the Tree Structure
        self.path = self.user_data_dir
        file_path = os.path.join(self.path, 'tree.json')
        
       
        self.store = JsonStore(file_path)
        
        return RootWidget()
    
         ## Function to load the state    
    def on_load(self):
        
        if self.store.exists('tree'):

            tree_data_to_load = self.store.get('tree')['tree_structure']
            data = tree_data_to_load
            
            self.root.treescreen.tree.root_options = {'text': data['text']}
            self.add_nodes_recursive(None, data['nodes'] )  
        else:
            print('Loading Defaults')  
        
        

    ## Function to add nodes recursivly on load
    def add_nodes_recursive(self, parent_widget, children_data):
       
        for child in children_data:
            
            if child['level'] == 3:
                node = self.root.treescreen.tree.add_node(
                MyClickableLabel(text=child['text'], is_open=child['is_open'], node_key = child['node_key']), 
                parent_widget
                )
                self.add_nodes_recursive(node, child['nodes'])
            else:
            
        
                node = self.root.treescreen.tree.add_node(
                MyTreeViewLabel(text=child['text'], is_open=child['is_open'], node_key = child['node_key']), 
                parent_widget
                )
                self.add_nodes_recursive(node, child['nodes'])

   
    ## Function to load data on start    
    def on_start(self):
       self.on_load() 
      
    ## Function to save data on pause
    def on_pause(self):
        self.on_save()
        
    ## Function to save data on stop
    def on_stop(self):
        self.on_save()
       
        

    ## Function to save the data
    def on_save(self):
       
        tree_data_to_save = self.serialize_tree( self.root.treescreen.tree.root)
        save_data = self.store.put('tree', tree_structure = tree_data_to_save )
        
        
        
     ## Function to serialize node and its children    
    def serialize_tree(self,node):

    # Base structure for a node(serialize each node)
       
        if hasattr(node, 'node_key'):
            print(node.node_key)
        else:
            print("Attribute not yet set")
            print(node)
        
        serialized_node = {
        'text': node.text,
        
        'is_open': node.is_open,
        'level': node.level,
        
        'node_key': node.node_key,
        
        
        
        'nodes': []
        }
       
    ## Recursively serialize children 
        for child in node.nodes:
            serialized_node['nodes'].append(self.serialize_tree(child))
        return serialized_node  
        

  
if __name__ == "__main__":
    MyTreeviewApp2().run()
