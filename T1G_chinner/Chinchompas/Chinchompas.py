import time
import utilities.api.item_ids as ids
import utilities.color as clr
import utilities.random_util as rd
from model.osrs.osrs_bot import OSRSBot
from model.runelite_bot import BotStatus
from utilities.api.morg_http_client import MorgHTTPSocket
from utilities.api.status_socket import StatusSocket
from utilities.geometry import RuneLiteObject
import pyautogui as pag
import model.osrs.Chinchompas.BotSpecImageSearch as imsearch
import utilities.game_launcher as launcher
import pathlib
import utilities.T1G_API as T1G_API
import utilities.ScreenToClient as stc
import utilities.BackGroundScreenCap as bcp
import utilities.RIOmouse as Mouse



    
class OSRSChinchompas(OSRSBot):
    api_m = MorgHTTPSocket()
    def __init__(self):
        bot_title = "ThatOneGuys ChinChompa Hunter"
        description = "Hunts ChinChompas"
        super().__init__(bot_title=bot_title, description=description)
        self.potion_to_make = None
        self.running_time = 1
        self.take_breaks = False
        self.break_length_min = 1
        self.break_length_max = 500
        self.time_between_actions_min =0.8
        self.time_between_actions_max =5
        self.potion_to_make = None
        self.mouse_speed = "medium"
        self.break_probabilty = 0.13
        self.Client_Info = None
        self.win_name = None
        self.pid_number = None
        self.Input = "failed to set mouse input"
        self.setupran = False
        self.alchedItems = 0

    def create_options(self):
        self.options_builder.add_slider_option("running_time", "How long to run (minutes)?", 1, 500)
        self.options_builder.add_checkbox_option("take_breaks", "Take breaks?", [" "])
        self.options_builder.add_slider_option("break_probabilty", "Chance to take breaks (percent)",1,100)
        self.options_builder.add_slider_option("break_length_min", "How long to take breaks (min) (Seconds)?", 1, 300)
        self.options_builder.add_slider_option("break_length_max", "How long to take breaks (max) (Seconds)?", 2, 300)    
        self.options_builder.add_checkbox_option("mouse_speed", "Mouse Speed (must choose & only select one)",[ "slowest", "slow","medium","fast","fastest"])
        self.options_builder.add_slider_option("time_between_actions_min", "How long to take between actions (min) (MiliSeconds)?", 600,3000)
        self.options_builder.add_slider_option("time_between_actions_max", "How long to take between actions (max) (MiliSeconds)?", 600,3000)
        
        self.options_builder.add_process_selector("Client_Info")
        self.options_builder.add_checkbox_option("Input","Choose Input Method",["Remote","PAG"])
        
                                               
    def save_options(self, options: dict):
        for option in options:        
            if option == "running_time":
                self.running_time = options[option]
            elif option == "take_breaks":
                self.take_breaks = options[option] != []
            elif option == "break_length_min":
                self.break_length_min = options[option]
            elif option == "break_length_max":
                self.break_length_max = (options[option])
            elif option == "mouse_speed":
                self.mouse_speed = options[option]
            elif option == "time_between_actions_min":
                self.time_between_actions_min = options[option]/1000
            elif option == "time_between_actions_max":
                self.time_between_actions_max = options[option]/1000
            elif option == "break_probabilty":
                self.break_probabilty = options[option]/100
                
            elif option == "Client_Info":
                self.Client_Info = options[option]
                client_info = str(self.Client_Info)
                win_name, pid_number = client_info.split(" : ")
                self.win_name = win_name
                self.pid_number = int(pid_number)
                self.win.window_title = self.win_name
                self.win.window_pid = self.pid_number
                stc.window_title = self.win_name
                Mouse.Mouse.clientpidSet = self.pid_number
                bcp.window_title = self.win_name
                bcp
            elif option == "Input":
                self.Input = options[option]
                if self.Input == ['Remote']:
                    Mouse.Mouse.RemoteInputEnabledSet = True
                elif self.Input == ['PAG']:
                    Mouse.Mouse.RemoteInputEnabledSet = False
                
                
            else:
                self.log_msg(f"Unknown option: {option}")
                print("Developer: ensure that the option keys are correct, and that options are being unpacked correctly.")
                self.options_set = False
                return
        self.log_msg(f"Running time: {self.running_time} minutes.")
        self.log_msg(f"Bot will{' ' if self.take_breaks else ' not '}take breaks.")
        self.log_msg(f"We are making {self.potion_to_make}s")
        self.log_msg("Options set successfully.")
        self.options_set = True
        
        

    def main_loop(self):
        start_time = time.time()
        end_time = self.running_time * 60
        print(self.mouse_speed)
        start_time = time.time()
        end_time = self.running_time * 60
        while time.time() - start_time < end_time:
            if rd.random_chance(probability=self.break_probabilty) and self.take_breaks:
                self.take_break(min_seconds =self.break_length_min, max_seconds=self.break_length_max, fancy=True)   
        
            self.update_progress((time.time() - start_time) / end_time)
            self.bot_loop_main()
        self.update_progress(1)
        self.log_msg("Finished.")
        self.logout()
        self.stop()
         
    
            

            
    def bot_loop_main(self):
        self.on_ground_Box_Trap()
        self.find_trap_catch()
        self.find_trap_no_catch()
       

        
        
    def on_ground_Box_Trap(self):
            on_ground_Box_Trap_Image = imsearch.BOT_IMAGES.joinpath("Chinchompas_IMG", "on_ground_Box_Trap.png")
    
            on_ground_Box_Trap = imsearch.search_img_in_rect(on_ground_Box_Trap_Image, self.win.game_view)
            
            if  on_ground_Box_Trap:
                self.mouse.move_to(on_ground_Box_Trap.random_point())
                Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
                time.sleep(Sleep_time)
                self.mouse.click()
                time.sleep(rd.fancy_normal_sample(5.5,6.5))
                self.on_ground_Box_Trap()
            
                        
    
                 
    def find_trap_no_catch(self):
        traps = self.get_all_tagged_in_rect(self.win.game_view, clr.RED)
        for trap in sorted(traps, key=RuneLiteObject.distance_from_rect_center):
            self.mouse.move_to(trap.random_point(), mouseSpeed=self.mouse_speed[0])
            if self.mouseover_text(contains="Reset", color=clr.OFF_WHITE):
                time.sleep(0.4)
                if self.mouseover_text(contains="Reset", color=clr.OFF_WHITE):
                    self.mouse.click()
                    time.sleep(rd.fancy_normal_sample(7.5,8.35))
            else:
                self.mouse.move_to(trap.random_point(), mouseSpeed=self.mouse_speed[0])
                if self.mouseover_text(contains="Reset", color=clr.OFF_WHITE):
                    time.sleep(0.4)
                    if self.mouseover_text(contains="Reset", color=clr.OFF_WHITE):
                        self.mouse.click()
                        time.sleep(rd.fancy_normal_sample(7.5,8.35))
                    
    def find_trap_catch(self):
        traps = self.get_all_tagged_in_rect(self.win.game_view, clr.PURPLE)
        for trap in sorted(traps, key=RuneLiteObject.distance_from_rect_center):
            self.mouse.move_to(trap.random_point(), mouseSpeed=self.mouse_speed[0])
            time.sleep(0.4)
            if self.mouseover_text(contains="Reset", color=clr.OFF_WHITE):
                self.mouse.click()
                time.sleep(rd.fancy_normal_sample(7.5,8.35))
            else:
                self.mouse.move_to(trap.random_point(), mouseSpeed=self.mouse_speed[0])
                time.sleep(0.4)
                if self.mouseover_text(contains="Reset", color=clr.OFF_WHITE):
                    self.mouse.click()
                    time.sleep(rd.fancy_normal_sample(7.5,8.35))
                    
    
    
              
    
                
    
            
            
  