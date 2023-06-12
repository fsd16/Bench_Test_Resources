from enphase_ecdc.pcu import PCU
from enphase_equipment.oscilloscope.agilent import AgilentDSO
from time import sleep
class PCU(PCU):

    def write_live_regs(self, datamodel_item, value):
        """Function to write to the live registers

        Args:
            datamodel_item (str): The datamodel address to write to
            value (any): the value to write to the register
        """
        self.log.info(f'Writing {datamodel_item} -> {value}')

        try:
            self.pcu.live_regs.search(datamodel_item).set_value(value)
        except AttributeError:
            top = datamodel_item.split('.')[0]
            self.log.info(f'The top level DatamodelItem "{top}" does not exist')
        except LookupError:
            self.log.info(f'The DatamodelItem "{datamodel_item}" does not exist')

    def read_live_regs(self, datamodel_item):
        """Function to read from the live registers

        Args:
            datamodel_item (str): The datamodel address to read from

        Returns:
            any: The value of the register
        """
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
        """Function to write to the dmir

        Args:
            datamodel_item (str): The datamodel address to write to
            value (any): the value to write to the dmir
        """
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
        """Function to read from the live registers

        Args:
            datamodel_item (str): The datamodel address to read from

        Returns:
            any: The value of the dmir
        """
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
    
    def wait_for_power(self):
        """Funciton to wait for for the PCU to begin to produce power
        """
        self.pcu.wait_for_boot()
        state = self.pcu.read_live_regs('RTDB.RTDB.Flags.power_enabled')
        while state == 0:
            state = self.pcu.read_live_regs('RTDB.RTDB.Flags.power_enabled')
            sleep(0.5)
        self.log.info(f'PCU producing power') 

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
        """Function to set the marker source

        Args:
            cursor (int): The cursor number: {1 | 2}
            source (int): The source channel number: {1 | 2 | 3 | 4}
        """
        self.write(f':MARKer:X{cursor}Y{cursor}source CHANnel{source}')

    def set_marker_position(self, cursor, axis, position, unit='s'):
        """Function to set the marker position

        Args:
            cursor (int): The cursor number: {1 | 2}
            axis (_type_): The cursor axis to set {Y| X}
            position (int): The position to set the cursor
            unit (str, optional): The units of the position supplied: {s | ms | us | ns | ps | Hz | kHz | MHz} Defaults to 's'.
        """
        self.write(f':MARKer:{axis}{cursor}Position {position} {unit}')

    def get_marker_postion(self, cursor, axis):
        """Funtion to get the marker postion

        Args:
            cursor (int): The cursor number: {1 | 2}
            axis (str): The cursor axis to get {Y| X}

        Returns:
            float: The marker postion recieved from the scope
        """
        return float(self.ask(f':MARKer:{axis}{cursor}Position?'))

    def get_marker_delta(self, axis):
        """Function get the delta between the cursors

        Args:
            axis (str): The cursor axis to get the delta along {Y| X}

        Returns:
            float: The cursor delta along the given axis received from the scope
        """
        return float(self.ask(f':MARKer:{axis}DELta?'))

    def display_labels(self, state):
        """Function to set the display state of the labels

        Args:
            status (str): The display state of the labels: {ON | OFF}
        """
        self.write(f':DISPLAY:LABEL {state}')

    def set_trigger_mode(self, mode):
        """Function to set the trigger sweep mode

        Args:
            mode (str): The trigger sweep mode: {AUTO | NORMal}
        """
        self.write(f':TRIGger:SWEep {mode}')

    def clear_status(self):
        """Function to clear the status data structures
        """
        self.write('*CLS')
    
    def get_triggered(self):
        """ Function to get the trigger state of the scope

        Returns:
            bool: The trigger state of the scope i.e True, False
        """
        return bool(int(self.ask(":TER?")))
    
    def set_aquisition_mode(self, control):
        """Function to set the aquisition mode.

        Args:
            control (str): the trigger control: {SINGle | RUN | STOP}
        """
        self.write(f':{control}')
    
    def set_aquisition_type(self, type):
        """Function to set the aquire type of the scope

        Args:
            type (str): The aquire type of the Scope: {NORMal | AVERage | HRESolution | PEAK}
        """
        self.write(f':ACQuire:TYPE {type}')

    def get_statistic(self, statistics):
        """Function to set the statistics returned by the scope

        Args:
            statistics (str): The statistics to be returned by the scope: {CURRent | MINimum | MAXimum | MEAN | STDDev | COUNt}
        """
        if statistics is 'ALL':
            statistics = 'ON'
        self.write(f':MEASure:STATistics {statistics}')
        stats = self.ask(f':MEASure:RESults?')
        return stats

    def get_statistics(self, statistics):
        self.write(f':MEASure:STATistics ON')
        stats = self.ask(f':MEASure:RESults?')
        return stats

    def display_statistics(self, state):
        """Function to set the display state of statisticson the scope

        Args:
            state (str): The display state of the statistics: {ON | OFF}
        """
        self.write(f':MEASure:STATistics:DISPlay {state}')

    def set_statistics_count(self, count):
        """Funtion to set the maxium number of values to use when calculating measurement statistics.

        Args:
            count (int): The max number of values to use when calculating measurement statistics
        """
        self.write(f':MEASure:STATistics:MCOunt {count}')

    def reset_statistics(self):
        """Function to reset the measurement statistics and zero count.
        """
        self.write(f':MEASure:STATistics:RESet')
    