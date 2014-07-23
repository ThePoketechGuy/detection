#!/usr/bin/env python
# -*- coding: utf-8 -*-
# window_ui.py
#
# Author: Yann KOETH
# Created: Wed Jul 16 19:06:25 2014 (+0200)
# Last-Updated: Wed Jul 23 21:16:01 2014 (+0200)
#           By: Yann KOETH
#     Update #: 382
#

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QPushButton,
                             QHBoxLayout, QVBoxLayout, QDesktopWidget, QScrollArea,
                             QLabel, QLineEdit, QListWidget, QComboBox, QDoubleSpinBox,
                             QSplitter, QGroupBox, QTextEdit, QAbstractItemView,
                             QSpinBox, QCheckBox)

from PyQt5.QtGui import QIcon, QDropEvent, QDragMoveEvent
from PyQt5.QtCore import QLocale

class QTreeView(QtWidgets.QTreeView):
    customSelectionChanged = QtCore.pyqtSignal(QtCore.QItemSelection, QtCore.QItemSelection)

    def __init__(self):
        super(QTreeView, self).__init__()

    def selectionChanged(self, *args, **kwds):
        self.customSelectionChanged.emit(*args, **kwds)
        super(QTreeView, self).selectionChanged(*args, **kwds)

class WindowUI():

    def widgetSource(self):
        """Create source widget.
        """
        hbox = QHBoxLayout()
        sourceLabel = QLabel(self.tr('Source'))

        self.sourceCBox = QComboBox(self)
        self.sourcePath = QLineEdit(self)
        self.sourcePath.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
#        self.sourcePath.setMinimumWidth(400)
        self.sourcePathButton = QPushButton('...')
        self.sourcePathButton.setMaximumWidth(40)

        self.playButton = QPushButton('')
        self.nextFrameButton = QPushButton('')
        self.refreshButton = QPushButton('')

        css = "QPushButton { border: none; }" \
            "QPushButton:pressed { border: 1px solid #555; background-color: #222; }"

        size = QtCore.QSize(23, 23)

        self.playButton.setIcon(QIcon('assets/pause.png'))
        self.playButton.setIconSize(size)
        self.playButton.setMinimumSize(size)
        self.playButton.setMaximumSize(size)
        self.playButton.setStyleSheet(css)

        self.refreshButton.setIcon(QIcon('assets/refresh.png'))
        self.refreshButton.setIconSize(size)
        self.refreshButton.setMinimumSize(size)
        self.refreshButton.setMaximumSize(size)
        self.refreshButton.setStyleSheet(css)


        self.nextFrameButton.setIcon(QIcon('assets/next.png'))
        self.nextFrameButton.setIconSize(size)
        self.nextFrameButton.setMinimumSize(size)
        self.nextFrameButton.setMaximumSize(size)
        self.nextFrameButton.setStyleSheet(css)

        self.sourceCBox.setCurrentIndex(0)

        controlsHbox = QHBoxLayout()
        controlsHbox.addWidget(self.playButton)
        controlsHbox.addWidget(self.nextFrameButton)
        controlsHbox.addWidget(self.refreshButton)
        controlsHbox.setAlignment(QtCore.Qt.AlignRight)

        hbox.addWidget(sourceLabel)
        hbox.addWidget(self.sourceCBox)
        hbox.addWidget(self.sourcePath)
        hbox.addWidget(self.sourcePathButton)
        hbox.addLayout(controlsHbox)
        hbox.setAlignment(QtCore.Qt.AlignLeft)
        return hbox

    def widgetFrame(self):
        """Create main display widget.
        """
        vbox = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setAlignment(QtCore.Qt.AlignCenter)
        self.mediaLabel = QLabel(self)
        scroll.setWidget(self.mediaLabel)
        vbox.addWidget(scroll)
        return vbox

    def widgetTree(self):
        """Create selected objects tree.
        """
        tree = QTreeView()
        tree.header().setHidden(True)
        tree.setDragEnabled(True)
        tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        tree.setDefaultDropAction(QtCore.Qt.MoveAction)
        tree.setDragDropMode(QAbstractItemView.InternalMove)
        tree.setAcceptDrops(True)
        tree.setDropIndicatorShown(True)
        return tree

    def widgetObjectList(self):
        """Create objects list widget.
        """
        self.objectsTree = self.widgetTree()
        self.availableObjectsList = QListWidget(self)
        self.availableObjectsList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.removeButton = QPushButton(self.tr('>>'))
        self.addButton = QPushButton(self.tr('<<'))

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.addButton)
        vbox.addWidget(self.removeButton)
        vbox.addStretch(1)

        vboxSelected = QVBoxLayout()
        selectedLabel = QLabel(self.tr('Selected'))
        selectedLabel.setAlignment(QtCore.Qt.AlignCenter)
        vboxSelected.addWidget(selectedLabel)
        vboxSelected.addWidget(self.objectsTree)
        vboxAvailable = QVBoxLayout()
        availableLabel = QLabel(self.tr('Available'))
        availableLabel.setAlignment(QtCore.Qt.AlignCenter)
        vboxAvailable.addWidget(availableLabel)
        vboxAvailable.addWidget(self.availableObjectsList)
        hbox = QHBoxLayout()
        hbox.addLayout(vboxSelected)
        hbox.addLayout(vbox)
        hbox.addLayout(vboxAvailable)
        return hbox

    def widgetClassifierDisplay(self):
        """Create classifier display widget.
        """
        self.colorPicker = QPushButton('')
        self.colorPicker.setMaximumSize(QtCore.QSize(16, 16))
        self.shapeCBox = QComboBox(self)
        self.fillCBox = QComboBox(self)
        self.fillPath = QPushButton('...')
        self.fillPath.setMaximumWidth(40)
        self.showName = QCheckBox(self.tr('Show Name'))

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(self.tr('Shape')))
        hbox.addWidget(self.shapeCBox)
        hbox.addWidget(self.fillCBox)
        hbox.addWidget(self.fillPath)
        hbox.addWidget(self.colorPicker)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addWidget(self.showName)
        vbox.addLayout(hbox)
        return vbox

    def widgetClassifierParameters(self):
        """Create classifier parameters widget.
        """
        hbox = QHBoxLayout()
        nameLabel = QLabel(self.tr('Name'))
        self.classifierName = QLineEdit(self)
        self.classifierType = QLabel('')
        hbox.addWidget(nameLabel)
        hbox.addWidget(self.classifierName)
        hbox.addWidget(self.classifierType)

        self.stabilize = QCheckBox(self.tr('Stabilize'))
        self.tracking = QCheckBox(self.tr('Tracking'))
        htracking = QHBoxLayout()
        htracking.addWidget(self.stabilize)
        htracking.addWidget(self.tracking)

        vlabel = QVBoxLayout()
        vparam = QVBoxLayout()

        self.scaleFactor = QDoubleSpinBox()
        self.scaleFactor.setMaximumWidth(65)
        self.scaleFactor.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.scaleFactor.setSingleStep(.1)
        self.scaleFactor.setDecimals(2)
        self.scaleFactor.setMinimum(1.1)
        self.minNeighbors = QSpinBox()
        self.minNeighbors.setMaximumWidth(65)
        self.minNeighbors.setMaximum(1500)
        self.minWidth = QSpinBox()
        self.minWidth.setMaximum(1500)
        self.minHeight = QSpinBox()
        self.minHeight.setMaximum(1500)
        self.autoNeighbors = QPushButton(self.tr("Auto"))
        self.autoNeighborsParam = QSpinBox()
        self.autoNeighborsParam.setMaximum(1500)
        self.autoNeighborsParam.setMaximumWidth(45)

        hminSize = QHBoxLayout()
        hminSize.addWidget(self.minWidth)
        hminSize.addWidget(QLabel(self.tr('x')))
        hminSize.addWidget(self.minHeight)
        hminSize.addStretch(1)

        vlabel.addWidget(QLabel(self.tr('Scale factor')))
        vlabel.addWidget(QLabel(self.tr('Min neighbors')))
        vlabel.addWidget(QLabel(self.tr('Minimum Size')))

        hNeighbors = QHBoxLayout()
        hNeighbors.addWidget(self.minNeighbors)
        hNeighbors.addWidget(self.autoNeighbors)
        hNeighbors.addWidget(self.autoNeighborsParam)
        hNeighbors.addStretch(1)

        vparam.addWidget(self.scaleFactor)
        vparam.addLayout(hNeighbors)
        vparam.addLayout(hminSize)

        hparameters = QHBoxLayout()
        hparameters.addLayout(vlabel)
        hparameters.addLayout(vparam)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(htracking)
        vbox.addLayout(hparameters)
        return vbox

    def widgetGlobalParam(self):
        """Create global parameters widget.
        """
        hbox = QHBoxLayout()
        self.displayCBox = QComboBox(self)
        self.bgCBox = QComboBox(self)
        self.bgColorPicker = QPushButton('')
        self.bgColorPicker.setMaximumSize(QtCore.QSize(16, 16))
        self.bgPathButton = QPushButton('...')
        self.bgPathButton.setMaximumWidth(45)
        hbox.addWidget(QLabel(self.tr('Display')))
        hbox.addWidget(self.displayCBox)
        hbox.addStretch(1)
        hbox.addWidget(QLabel(self.tr('Background')))
        hbox.addWidget(self.bgCBox)
        hbox.addWidget(self.bgColorPicker)
        hbox.addWidget(self.bgPathButton)

        self.equalizeHist = QCheckBox(self.tr('Equalize histogram'))

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.equalizeHist)
        return vbox

    def widgetParameters(self):
        """Create parameters widget.
        """
        globalParamBox = QGroupBox(self.tr('Global parameters'))
        objects = self.widgetGlobalParam()
        globalParamBox.setLayout(objects)

        detectBox = QGroupBox(self.tr('Detect'))
        objects = self.widgetObjectList()
        detectBox.setLayout(objects)

        self.displayBox = QGroupBox(self.tr('Classifier Display'))
        display = self.widgetClassifierDisplay()
        self.displayBox.setLayout(display)

        self.parametersBox = QGroupBox(self.tr('Classifier Parameters'))
        parameters = self.widgetClassifierParameters()
        self.parametersBox.setLayout(parameters)

        vbox = QVBoxLayout()
        vbox.addWidget(globalParamBox)
        vbox.addWidget(detectBox)
        vbox.addWidget(self.displayBox)
        vbox.addWidget(self.parametersBox)
        return vbox

    def widgetDebug(self):
        """Create debug infos widget.
        """
        self.debugText = QTextEdit(self)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.showDetails = QPushButton(self.tr('Details >>>'))
        self.showDetails.setCheckable(True)
        self.showDetails.setChecked(1)
        hbox.addWidget(self.showDetails)
        hbox.addStretch(1)

        vbox.addLayout(hbox)
        vbox.addWidget(self.debugText)
        vbox.addStretch(1)

        return vbox

    def setupUI(self):
        """Create User Interface.
        """
        sourceWidget = self.widgetSource()
        frameWidget = self.widgetFrame()
        parametersWidget = self.widgetParameters()

        leftSide = QWidget()
        leftSide.setLayout(parametersWidget)
        rightSide = QWidget()
        rightSide.setLayout(frameWidget)
        self.hsplitter = QSplitter(QtCore.Qt.Horizontal)
        self.hsplitter.addWidget(leftSide)
        self.hsplitter.addWidget(rightSide)
        self.hsplitter.setStretchFactor(0, 1)
        self.hsplitter.setStretchFactor(1, 10)

        downSide = QWidget()
        downSide.setLayout(self.widgetDebug())
        self.vsplitter = QSplitter(QtCore.Qt.Vertical)
        self.vsplitter.addWidget(self.hsplitter)
        self.vsplitter.addWidget(downSide)
        self.vsplitter.setStretchFactor(0, 10)
        self.vsplitter.setStretchFactor(1, 1)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(sourceWidget)
        mainLayout.addWidget(self.vsplitter)
        self.setLayout(mainLayout)
        self.setGeometry(300, 300, 800, 600)
        self.show()
