import copy
import re


def svg_id_prepend(root, prefix):
    """Append prefix to id attributes and url(#id) references."""
    root = copy.deepcopy(root)

    id_attributes = {}
    # Replace id attributes
    for e in root.findall("*//*[@id]"):
        idvalue = e.attrib['id']
        newidvalue = prefix + idvalue
        e.attrib['id'] = newidvalue

        id_attributes[idvalue] = newidvalue

    # Update references
    for e in root.xpath("//*[contains(@*, 'url(#')]"):
        for attr, value in e.attrib.items():
            matchobj = re.match('url\(#(.*)\)', value)
            if matchobj and matchobj.groups()[0] in id_attributes:
                e.attrib[attr] = 'url(#%s)' % id_attributes[matchobj.groups()[
                    0]]

    return root


class Unit:
    """Implementation of SVG units and conversions between them.

    Parameters
    ----------
    measure : str
        value with unit (for example, '2cm')
    """
    per_inch = {'px': 90,
                'cm': 2.54,
                'mm': 25.4,
                'pt': 1
                }

    def __init__(self, measure):
        try:
            self.value = float(measure)
            self.unit = 'px'
        except ValueError:
            m = re.match('([0-9]+\.?[0-9]*)([a-z]+)', measure)
            value, unit = m.groups()
            self.value = float(value)
            self.unit = unit

    def to(self, unit):
        """Convert to a given unit.

        Parameters
        ----------
        unit : str
           Name of the unit to convert to.

        Returns
        -------
        u : Unit
            new Unit object with the requested unit and computed value.
        """
        u = Unit("0cm")
        u.value = self.value/self.per_inch[self.unit]*self.per_inch[unit]
        u.unit = unit
        return u

    def __str__(self):
        return "{}{}".format(self.value, self.unit)

    def __repr__(self):
        return "Unit({})".format(str(self))

    def __mul__(self, number):
        u = Unit("0cm")
        u.value = self.value * number
        u.unit = self.unit
        return u

    def __truediv__(self, number):
        return self * (1./number)

    def __div__(self, number):
        return self * (1./number)
