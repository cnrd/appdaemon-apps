import appdaemon.plugins.hass.hassapi as hass

import time

from datetime import datetime, timedelta

class switchHandler(hass.Hass):
  
  def initialize(self):
    self.listen_event(self.button_press, "deconz_event")
    self.switch_id_dict = {}

  def button_press(self, event_name, data, kwargs):
    switch_id = data['id'].lower().replace(" ", "_")
    event = data['event']

    if (switch_id == 'tradfri_remote_living_room' and
        event == 5002):
      self.log("Switches in dict: " + str(self.switch_id_dict))
    if (switch_id.startswith('lumisensor_switch') or
        switch_id.startswith('switch_')):
      if switch_id not in self.switch_id_dict:
        self.switch_id_dict[switch_id] = time.time()

      if event == 1000:
        self.switch_id_dict[switch_id] = time.time()

      if event == 1002:
        click_time = time.time() - self.switch_id_dict[switch_id]
        if click_time < 0.8:
          self.send_event(switch_id, "single")
        elif click_time >= 0.8 and click_time < 10.0:
          self.send_event(switch_id, "long_click_press")
        else:
          self.send_event(switch_id, "super_long_click_press")

      if event == 1004:
        self.send_event(switch_id, "double")

      if event == 1005:
        self.send_event(switch_id, "triple")

      if event == 1006:
        self.send_event(switch_id, "quadruple")

  def send_event(self, switch_id, click_type):
    self.fire_event("click", entity_id = switch_id, click_type = click_type)
    self.log("Sending click_type: " + click_type + ", entity_id: " + switch_id)