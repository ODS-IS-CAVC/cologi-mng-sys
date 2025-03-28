# Copyright 2025 Intent Exchange, Inc.
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the “Software”), to deal in the Software without
# restriction, including without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from flask import Blueprint, render_template
from ..models.trsp_vehicle_trms_model import TrspVehicleTrms

trsp_vehicle_trms_views=Blueprint('trsp_vehicle_trms_views', __name__)

@trsp_vehicle_trms_views.route('/trsp_vehicle_trms')
def trsp_vehicle_trms_list():
    trsp_vehicle_trmss='sample data'
    trsp_vehicle_trmss=TrspVehicleTrms.query.all()
    print(trsp_vehicle_trmss)
    return render_template('trsp_vehicle_trms/trsp_vehicle_trms_list.html', trsp_vehicle_trmss=trsp_vehicle_trmss)