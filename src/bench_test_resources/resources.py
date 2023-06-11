from enphase_ecdc.pcu import PCU
from enphase_equipment.oscilloscope.agilent import AgilentDSO

class PCU(PCU):

    def write_live_regs(self, datamodel_item, value):

        self.log.info(f'Writing {datamodel_item} -> {value}')

        try:
            self.pcu.live_regs.search(datamodel_item).set_value(value)
        except AttributeError:
            top = datamodel_item.split('.')[0]
            self.log.info(f'The top level DatamodelItem "{top}" does not exist')
        except LookupError:
            self.log.info(f'The DatamodelItem "{datamodel_item}" does not exist')

    def read_live_regs(self, datamodel_item):

        try:
            value = self.pcu.live_regs.search(datamodel_item).get_value()
            self.log.info(f'{datamodel_item} = {value}')
            return value
        except AttributeError:
            top = datamodel_item.split('.')[0]
            self.log.info(f'The top level DatamodelItem "{top}" does not exist')
            return None
        except LookupError:
            self.log.info(f'The DatamodelItem "{datamodel_item}" does not exist')
            return None
    
    def write_dmir(self, datamodel_item, value, area=0, bank=20):
        self.log.info(f'Writing {datamodel_item} -> {value}')
        top = datamodel_item.split('.')[0]
        try:
            attr = getattr(self.dm, top)
            dmir = self.get_dmir(attr, area, bank)
            try:
                dmir.search(datamodel_item).set_value(value)
            except LookupError:
                self.log.info(f'The DatamodelItem "{datamodel_item}" does not exist')
        except AttributeError:
            self.log.info(f'The top level DatamodelItem "{top}" does not exist')
    
    def read_dmir(self, datamodel_item, area=0, bank=20):
        self.log.info(f'Writing {datamodel_item} -> {value}')
        top = datamodel_item.split('.')[0]
        try:
            attr = getattr(self.dm, top)
            dmir = self.get_dmir(attr, area, bank)
            try:
                value = dmir.search(datamodel_item).get_value()
                self.log.info(f'{datamodel_item} = {value}')
                return value
            except LookupError:
                self.log.info(f'The DatamodelItem "{datamodel_item}" does not exist')
                return None
        except AttributeError:
            self.log.info(f'The top level DatamodelItem "{top}" does not exist')
            return None

class Scope(AgilentDSO):

    def set_channel_label(self, channel, label):
        """ Function to set a channels label

        Args:
            channel (int): The number of the channel for the setting e.g 1
            label (str): The label for the channel
        """
        self.write(f':CHANnel{channel}:LABel "{label}"')
    
    def set_channel_labels(self, ch1, ch2, ch3, ch4):
        """Function to set all channel labels at once

        Args:
            ch1 (str): The label for channe1 1
            ch2 (str): The label for channe1 2
            ch3 (str): The label for channe1 3
            ch4 (str): The label for channe1 4
        """
        self.write(f':CHAN1:LABel "{ch1}";:CHAN2:LABel "{ch2}";:CHAN3:LABel "{ch3}";:CHAN4:LABel "{ch4}"')
    
    def set_channel_measurement(self, channel, type):
        """ Function to set a measurement type for a channel

        Args:
            channel (int): The number of the channel for the setting e.g 1
            type (str): The measurement type e.g 'VMAX'
        """
        self.write(f':MEAS:{type} CHANnel{channel}')
    
    def get_channel_measurement(self, channel, type):
        """ Function to get the measurement value for a channel

        Args:
            channel (int): The number of the channel for the setting e.g 1
            type (str): The measurement type e.g 'VMAX'

        Returns:
            float: The measurement received from the scope
        """
        return float(self.ask(f':MEASure:{type}? CHANnel{channel}'))
    
    def set_marker_source(self, cursor, source):
        self.write(f':MARKer:X{cursor}Y{cursor}source CHANnel{source}')

    def set_marker_position(self, cursor, axis, position, unit='s'):
        self.write(f':MARKer:{axis}{cursor}Position {position} {unit}')

    def get_marker_postion(self, cursor, axis):
        return float(self.ask(f':MARKer:{axis}{cursor}Position?'))

    def get_marker_delta(self, axis):
        return float(self.ask(f':MARKer:{axis}DELta?'))

    def display_labels(self, status):
        self.write(f':DISPLAY:LABEL {status}')

    def set_trigger_mode(self, mode):
        self.write(f':TRIGger:SWEep {mode}')
    
    def set_trigger_control(self, control):
        self.write(f':{control}')

    def clear_trigger(self):
        self.write('*CLS')
    
    def get_triggered(self):
        """ Function to get the trigger state of the scope

        Returns:
            bool: The trigger state of the scope i.e True, False
        """
        return bool(int(self.ask(":TER?")))