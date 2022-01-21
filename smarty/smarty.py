# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Smarty
                                 A QGIS plugin
 Smarty attempt
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2022-01-19
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Smarty
        email                : caroline@smarty.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsProject, Qgis

#########
from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup as StreetLookup
#########

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .smarty_dialog import SmartyDialog
import os.path


class Smarty:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        # import pip
        # pip._internal.main(['install', 'smartystreets_python_sdk'])
        # import subprocess
        # import sys
        # #subprocess.check_call([sys.executable, "-m", "pip", "install", "smartystreets_python_sdk"])
        # subprocess.call(['pip', 'install', 'smartystreets_python_sdk'])

        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Smarty_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Smarty')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Smarty', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/smarty/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Smarty'),
                action)
            self.iface.removeToolBarIcon(action)

    def smarty(self):
    
        auth_id = "c21cabd2-1a89-7746-e799-d35d70d7080b"
        auth_token = "nD3IIoyZ3H4LSzNp6qpl"

        credentials = StaticCredentials(auth_id, auth_token)

        client = ClientBuilder(credentials).with_licenses(["us-rooftop-geo"]).build_us_street_api_client()

        lookup = StreetLookup()
        #lookup.input_id = "24601"  # Optional ID from your system ##################################
        
        lookup.addressee = self.dlg.addressee.text()  
        lookup.street = self.dlg.street.text() 
        lookup.street2 = self.dlg.street2.text()
        lookup.secondary = self.dlg.secondary.text()
        lookup.urbanization = self.dlg.urbanization.text() 
        lookup.city = self.dlg.city.text() 
        lookup.state = self.dlg.state.text() 
        lookup.zipcode = self.dlg.zipcode.text()
        #### lookup.candidates = self.dlg.candidates.text().toInt()   #### just took candidates off the form :]
        lookup.candidates = 3
        lookup.match = "invalid" ### just took match off the form :]

        try:
            client.send_lookup(lookup)
        except exceptions.SmartyException as err:
            self.iface.messageBar().pushMessage("FAIL: ", "Goodbye, world! LINE: 216", level=Qgis.Critical, duration=3)
            return

        result = lookup.result

        if not result:
            self.iface.messageBar().pushMessage("NO MATCH: ", "Goodbye, world! LINE 223", level=Qgis.Critical, duration=3)
            return

        first_candidate = result[0]

        message = ("Address is valid. (There is at least one candidate)" + "\nZIP Code: " + first_candidate.components.zipcode + 
            "\nCounty: " + first_candidate.metadata.county_name + "\nLatitude: {}".format(first_candidate.metadata.latitude) + 
            "\nLongitude: {}".format(first_candidate.metadata.longitude))

        self.iface.messageBar().pushMessage("Success: ", message, level=Qgis.Critical, duration=3)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = SmartyDialog()
            self.dlg.pushButton.clicked.connect(self.smarty)

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
