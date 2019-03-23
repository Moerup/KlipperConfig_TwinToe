
# -*- coding: utf-8 -*-

from nukeToMari import exportToMari
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import time
import random
import os

# - Import Nuke to Mari - (remember to set the nuke.pluginAddPath() to script location) - #

import nukeToMari
reload(nukeToMari)

# - #

version = "1.0"
hexcolor = [3427881471, 3427890943, 3427900415, 3427909631, 3008482559, 2387725567, 1783745791, 1365101823, 1367526655, 1369951487,
            1372376319, 1372366847, 1372357375, 1372347903, 1791775231, 2395755007, 3016511999, 3435090431, 3432731135, 3430306303]

onek = '1024 1024 - 1024'
twok = '2048 2048 - 2048'
fourk = '4096 4096 - 4096'
eightk = '8192 8192 - 8192'

for f in [onek, twok, fourk, eightk]:
    nuke.addFormat(f)


class materialTool(QWidget):
    def __init__(self):
        super(materialTool, self).__init__(None, Qt.WindowStaysOnTopHint)
        self.font = QFont('SansSerif', 9)
        # LAYOUTS
        self.viewerlayout = QGridLayout()
        self.matsetlayout = QVBoxLayout()
        self.astsetlayout = QGridLayout()
        self.browserlayout = QVBoxLayout()
        self.mainLayout = QVBoxLayout()

        # LAYOUTSTYLE

        self.viewerlayout.setContentsMargins(0, 0, 0, 8)
        self.matsetlayout.setContentsMargins(0, 0, 0, 0)
        self.astsetlayout.setContentsMargins(0, 0, 0, 0)

        # LAYOUT ONE WIDGETS

        self.swapbrowser_ui = QPushButton("materials")
        self.swapbrowser_ui.setFont(self.font)
        self.passview_ui = QComboBox()
        self.passview_ui.addItem("select channel to view")
        self.passview_ui.setMinimumWidth(300)
        self.paths_ui = QPushButton("show settings")
        self.paths_ui.setFont(self.font)

        # ADD TO LAYOUT ONE
        self.viewerlayout.addWidget(self.passview_ui, 0, 0, 1, 2)
        self.viewerlayout.addWidget(self.paths_ui, 1, 0, 1, 1)
        self.viewerlayout.addWidget(self.swapbrowser_ui, 1, 1, 1, 1)

        # LAYOUT TWO WIDGETS
        self.matpath = QLineEdit()
        self.matpath.setPlaceholderText("MATERIAL LIBRARY PATH")
        self.matpath.setObjectName('matobject')
        self.nuketomari = QPushButton("export to mari")
        self.assetname = QComboBox()
        self.resolution = QComboBox()

        for r in ["- 1024", "- 2048", "- 4096", "- 8192"]:
            self.resolution.addItem(r)

        self.newasset = QPushButton("new asset")
        self.uvpath = QLineEdit()
        self.uvpath.setPlaceholderText("UV MASK PATH")
        self.uvpath.setObjectName('uvobject')
        self.mskpath = QLineEdit()
        self.mskpath.setObjectName('mskobject')
        self.mskpath.setPlaceholderText("MASK PATH")

        # ADD TO LAYOUT TWO
        self.settingslayouts = [
            self.assetname, self.newasset, self.uvpath, self.mskpath, self.resolution]
        self.matsetlayout.addWidget(self.matpath)
        self.matsetlayout.addWidget(self.nuketomari)
        self.astsetlayout.addWidget(self.assetname, 0, 0, 1, 2)
        self.astsetlayout.addWidget(self.resolution, 0, 2, 1, 1)
        self.astsetlayout.addWidget(self.newasset, 1, 0, 1, 3)
        self.astsetlayout.addWidget(self.uvpath, 2, 0, 1, 3)
        self.astsetlayout.addWidget(self.mskpath, 3, 0, 1, 3)

        for w in self.settingslayouts:
            w.setFont(self.font)
            w.setHidden(True)

        self.matpath.setHidden(True)
        self.nuketomari.setHidden(True)
        self.settingslayouts.append(self.matpath)
        self.settingslayouts.append(self.nuketomari)

        # ADD TO MAIN LAYOUT
        for w in [self.viewerlayout, self.browserlayout, self.matsetlayout, self.astsetlayout]:
            self.mainLayout.addLayout(w)

        self.setLayout(self.mainLayout)
        self.setWindowTitle('no asset found')
        self.mainLayout.setSizeConstraint(self.mainLayout.SetFixedSize)

        # - BUILD UI - #
        self.buildUi()
        # - BUILD UI - #
        self.signals()

    # - Functions to add signals (this is to avoid signal calling on build) - #
    def signals(self):
        self.swapbrowser_ui.clicked.connect(self.browserSwap)
        self.passview_ui.currentIndexChanged.connect(self.viewerswitch)
        self.paths_ui.clicked.connect(self.showHideSettings)
        self.nuketomari.clicked.connect(self.exporter)
        self.assetname.activated.connect(self.buildUi)
        self.resolution.activated.connect(self.resolutionChange)
        self.newasset.clicked.connect(self.createasset)
        self.uvpath.textChanged.connect(self.pathchange)
        self.matpath.textChanged.connect(self.pathchange)
        self.mskpath.textChanged.connect(self.pathchange)

    # - Function for building the browser UI                              - #
    def buildUi(self):
        self.settingsCheck()
        self.paths()
        self.clearLayout()
        print("Building user interface! - textureBuilder - v"+version)
        itemlist = []

        if self.swapbrowser_ui.text() == "materials":
            [itemlist.append(i) for i in os.walk(materiallocation).next()[1]]
        else:
            [itemlist.append(i) for i in os.walk(masklocation).next()[1]]

        print(itemlist)

        # BUILDING ITEMS
        if itemlist:
            for i in itemlist:
                # ITEM LAYOUT
                self.itemlayout = QHBoxLayout()
                self.frame = QFrame()
                self.frame.setStyleSheet("background-color: rgb(72,72,72)")
                self.frame.setLayout(self.itemlayout)
                self.itemicon = QPushButton("◑")
                self.itemicon.setMaximumWidth(25)
                self.itemicon.setMaximumHeight(25)
                self.itemlabel = QPushButton(i)
                # self.itemlabel.setFont(self.font)
                self.itemlabel.clicked.connect(self.importitem)
                self.itemlabel.setMaximumHeight(25)

                # ADD TO ITEM LAYOUT
                for w in [self.itemicon, self.itemlabel]:
                    self.itemlayout.addWidget(w)

                self.browserlayout.addWidget(self.frame)

    # - Function for clearing the browser layout                           - #
    def clearLayout(self):
        print("clear layout")
        layout = self.browserlayout
        for i in reversed(range(layout.count())):
            layout.takeAt(i).widget().deleteLater()

    # - Global variables for asset,filepath,masklocation,material location - #
    def paths(self):
        asset = self.assetname.currentText()
        filepath = self.matpath.text()
        masklocation = self.mskpath.text()
        materiallocation = self.matpath.text()

        global asset
        global filepath
        global masklocation
        global materiallocation

        print ("ASSET : "+asset)
        print ("")
        print ("MASKS : "+masklocation)
        print ("MATERIALS : "+materiallocation)
        print ("")

    # - Function that scans scene for settings files                       - #
    def settingsCheck(self):
        print ("settings check")
        for n in nuke.allNodes(recurseGroups=True):
            if n['label'].value() == 'texBuilder':
                self.assetname.addItem(n.name())
                self.matpath.setText(n['matpath'].value())
                uvmaskpathnuke = nuke.toNode(n.name())['uvmskpath'].value()
                self.uvpath.setText(uvmaskpathnuke)
                maskpathnuke = nuke.toNode(n.name())['mskpath'].value()
                self.mskpath.setText(maskpathnuke)
                resolutionnuke = nuke.toNode(n.name())['matresolution'].value()
                index = self.resolution.findText(
                    resolutionnuke, Qt.MatchFixedString)
                self.resolution.setCurrentIndex(index)
                self.setWindowTitle(n.name())

    # - UTILITY - Function for running the nuke to mari exporter          - #
    def exporter(self):
        print ("exporter")
        exportToMari(asset, filepath, masklocation, materiallocation)

    # - UTILITY - Function for global resolution change                   - #
    def resolutionChange(self):
        print ("resolution change")
        res = self.sender().currentText()
        for n in nuke.allNodes(recurseGroups=True):
            if n['label'].value() == asset+'_FORMAT':
                n['format'].setValue(res)
        nuke.toNode(asset)['matresolution'].setValue(res)

    # - UTILITY - Function for changing paths in the UI                  - #
    def pathchange(self):
        print ("path change")
        object = self.sender().objectName()
        nukenode = nuke.toNode(str(self.assetname.currentText())
        if object == "uvobject":
            nukenode['uvmskpath'].setText(self.sender().text())
        if object == "mskobject":
            nukenode['mskpath'].setText(self.sender().text())
        if object == "matobject":
            for n in nuke.allNodes(recurseGroups=True):
                try:
                    n['matpath'].setText(self.sender().text())
                except:
                    pass
        self.buildUi()

    # - UTILITY - Function for creating a new asset                     - #
    def createasset(self):
        print "create asset"
        nodename, ok = QInputDialog.getText(self, '', 'unique asset name:')
        if ok:
            nodeExists = bool([n for n in nuke.allNodes(
                recurseGroups=True) if n.name() == nodename])
            if not nodeExists:
                print "create asset"
                settingsnode = nuke.nodes.Group(
                    name=nodename, label='texBuilder')
                matlocation = nuke.String_Knob(
                    "matpath", "material library location : ", "")
                matlocation.setEnabled(False)
                uvmask = nuke.File_Knob("uvmskpath", "uv mask file : ")
                uvmask.setEnabled(False)
                msklocation = nuke.String_Knob(
                    "mskpath", "mask location : ", "")
                msklocation.setEnabled(False)
                matlocation = nuke.String_Knob(
                    "matpath", "material library location : ", "")
                matlocation.setEnabled(False)
                matresolution = nuke.String_Knob(
                    "matresolution", "resolution : ", "- 4096")
                matresolution.setEnabled(False)
                for k in [matlocation, uvmask, msklocation, matresolution]:
                    settingsnode.addKnob(k)
                settingsnode['matpath'].setValue(self.matpath.text())
                self.assetname.addItem(nodename)
                index = self.assetname.findText(nodename, Qt.MatchFixedString)
                self.assetname.setCurrentIndex(index)
                with settingsnode:
                    o = nuke.nodes.Output()
                    i = nuke.nodes.Input()
                    o.setInput(0, i)
                self.settingsCheck()
            else:
                QMessageBox.information(
                    self, '', "Please select unique name!", QMessageBox.Ok)
                self.createasset()

    # - UTILITY - Function for swapping brower                              - #
    def browserSwap(self):
        print "swapping browser"
        mode = self.sender().text()
        if mode == "materials":
            self.sender().setText("masks")
        if mode == "masks":
            self.sender().setText("materials")
        self.buildUi()

    # - UTILITY - Function for importing items from the browser UI          - #
    def importitem(self):
        print "importing item"
        item = self.sender().text()
        itemname = self.assetname.currentText()+"_"+item
        if self.swapbrowser_ui.text() == "masks":
            self.itempath = self.mskpath.text()
            basepath = os.path.join(self.itempath, item)
            msknode = nuke.nodes.Group(
                name=itemname, label="MASK", tile_color=255, note_font="Bitstream Vera Sans Bold")
            with msknode:
                read = nuke.nodes.Read(name="read", on_error="black", raw=True)
                uvread = nuke.nodes.Read(
                    name="uvread", on_error="black", raw=True)
                erode = nuke.nodes.Dilate(name="dilate", size=1)
                maskmerge = nuke.nodes.Merge2(
                    name="maskmerge", operation="multiply")
                out = nuke.nodes.Output()
                reformatuv = nuke.nodes.Reformat(label=self.assetname.currentText(
                )+"_FORMAT", format=self.resolution.currentText())
                reformatread = nuke.nodes.Reformat(label=self.assetname.currentText(
                )+"_FORMAT", format=self.resolution.currentText())
                reformatread.setInput(0, read)
                maskmerge.setInput(0, reformatread)
                maskmerge.setInput(1, reformatuv)
                reformatuv.setInput(0, erode)
                erode.setInput(0, uvread)
                out.setInput(0, maskmerge)
                baseuvpath = os.path.dirname(self.uvpath.text())
                uvpath = os.path.join(
                    baseuvpath, nuke.getFileNameList(baseuvpath)[0])
                filepath = os.path.join(
                    basepath, nuke.getFileNameList(basepath)[0])
                read['file'].fromUserText(filepath)
                uvread['file'].fromUserText(uvpath)

        if self.swapbrowser_ui.text() == "materials":
            self.itempath = self.matpath.text()
            basepath = os.path.join(self.itempath, item)
            matnode = nuke.nodes.Group(name=itemname, label="MATERIAL", tile_color=random.choice(
                hexcolor), note_font="Bitstream Vera Sans Bold")
            with matnode:
                output = nuke.nodes.Output(name="out")
                input = nuke.nodes.Input(name="in")
                mask = nuke.nodes.Input(name="mask")
                passmerge = nuke.nodes.Merge2(
                    name="passMerge", also_merge="all", operation="plus")
                merge = nuke.nodes.Merge2(
                    name="materialMerge", also_merge="all", operation="copy")
                alphashuffle = nuke.nodes.Shuffle(
                    name=self.assetname.currentText()+"AlphaShuffle", out="alpha")
                output.setInput(0, merge)
                merge.setInput(2, alphashuffle)
                merge.setInput(1, passmerge)
                alphashuffle.setInput(0, mask)
                merge.setInput(0, input)
                # merge['maskChannelInput'].setValue(True)

                for f in os.listdir(basepath):
                    nuke.Layer(
                        f, [f+'.red', f+'.green', f+'.blue', f+'.alpha'])
                    filepath = os.path.join(basepath, f, f+".1001.tif")
                    read = nuke.nodes.Read(
                        name=f, on_error="black", raw=True, label="CHANNEL")
                    read['file'].setValue(filepath)
                    shuffle = nuke.nodes.Shuffle(name=f+"Shuffle")
                    shuffle['in'].setValue('rgba')
                    shuffle['out'].setValue(f)
                    reformat = nuke.nodes.Reformat(label=self.assetname.currentText(
                    )+"_FORMAT", format=self.resolution.currentText())
                    reformat.setInput(0, read)
                    shuffle.setInput(0, reformat)
                    passmerge.connectInput(0, shuffle)
        self.reloadviewer()

    # - UTILITY - Function for reloading the viewer                         - #
    def reloadviewer(self):
        print "reloading viewer"
        channels = []
        self.passview_ui.clear()
        for n in nuke.allNodes(recurseGroups=True):
            if n['label'].value() == "CHANNEL":
                channels.append(n['name'].value())
        channelssorted = sorted(set(channels))
        channelssorted.insert(0, "rgba")
        for c in channelssorted:
            self.passview_ui.addItem(c)

    # - UTILITY - Function for switching viewers                            - #
    def viewerswitch(self):
        print "switching viewer"
        channel = self.passview_ui.currentText()
        for n in nuke.allNodes(recurseGroups=True):
            if n.Class() == "Viewer":
                n.knob('channels').setValue(channel)

    # - UTILITY - Function for showing and hiding parts of the  UI         - #
    def showHideSettings(self):
        if self.sender().text() == "show settings":
            self.matsetlayout.setContentsMargins(0, 8, 0, 4)
            self.astsetlayout.setContentsMargins(0, 4, 0, 0)
            self.sender().setText("hide settings")
            # ADD TO LAYOUT TWO
            for w in self.settingslayouts:
                w.setHidden(False)

        elif self.sender().text() == "hide settings":
            self.matsetlayout.setContentsMargins(0, 0, 0, 0)
            self.astsetlayout.setContentsMargins(0, 0, 0, 0)
            self.sender().setText("show settings")
            for w in self.settingslayouts:
                w.setHidden(True)


panel = materialTool()
panel.show()
