from os.path import dirname, join

from sila2.framework import Feature

Ot2ControllerFeature = Feature(open(join(dirname(__file__), "Ot2Controller.sila.xml")).read())
