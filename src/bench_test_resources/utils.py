from typing import Dict, Any, TypeVar
from pathlib import Path

def dict_value_to_index(dict, value):
    return list(dict.values()).index(value)

KeyType = TypeVar('KeyType')
def deep_update(mapping: Dict[KeyType, Any], *updating_mappings: Dict[KeyType, Any]) -> Dict[KeyType, Any]:
        updated_mapping = mapping.copy()
        for updating_mapping in updating_mappings:
            for k, v in updating_mapping.items():
                if k in updated_mapping and isinstance(updated_mapping[k], dict) and isinstance(v, dict):
                    updated_mapping[k] = deep_update(updated_mapping[k], v)
                else:
                    updated_mapping[k] = v

        return updated_mapping

# Ensure file name is unique
def uniquify(filepath):
    filepath_P = Path(filepath)
    counter = 1

    while filepath_P.exists():
        filepath_P = f"{filepath_P.stem} ({counter}){filepath_P.suffix}"
        counter += 1

    return filepath_P

class InterpMulti:
    def __init__(self, data, k=3, *args, **kwargs):
        
        """Class to extend Univariate Spline to handle multi curves. Given x, y curve data and a corresponding variable, v, a point can be interpolated at a chosen x point and v value.

        Args:
            curves (list): List of mapping objects containing array like objects of x, y, and varible data. e.g [{'x': x1_array, 'y': y1_array, 'v': v1}, {'x': x2_array, 'y': y2_array, 'v': v2}, ...]. Variable value must be increasing
            k (int, optional): Degree of the smoothing spline. Must be 1 <= k <= 5. k = 3 is a cubic spline. Defaults to 3.
        """
        super().__init__(*args, **kwargs)
        
        self.curve_models = [UnivariateSpline(d['x'], d['y'], k=k) for d in data]
        self.variables = array([d['v'][0] for d in data])

    def get_point(self, x, v):
        """Given the value x and the variable v, return the point y.

        Args:
            x (float): Point x to evaluate y at
            v (float): Variable v to evaluate y for.

        Returns:
            float: Interpolated y value for a given x and v.
        """
        y_options = [curve_model(x)  for curve_model in self.curve_models]
        
        uS = UnivariateSpline(self.variables, y_options, k=2)
        
        y = uS(v)
        
        return float(y)