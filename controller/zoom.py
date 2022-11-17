"""
Changing the focal point of the data set

The ZOOM relates to how small of a time window we care about
The FOCUS relates to where in the timeline the focus should be
"""

import view.View_dm
from model.Model_dm import Model_dm




def zoom(win, dm: Model_dm, values) -> str:
    """
    Change the amount we're zoomed in
    """
 
    z_val = float(values['-ZOOM-']) # This is a percentage.
    z_ratio = z_val / 100           # Fractional version.
    if dm.DEBUG_ZOOM:
        print(f"Zoom set to: {round(z_ratio, 2)}")
    min, max = dm.cert_min, dm.cert_max

    # How many dates do we have?
    date_cnt = len(dm.cert_range)
    if dm.DEBUG_ZOOM:
        print(f"DC: {date_cnt}")
    if date_cnt < 1:
        return("No data")
    # Over what range are those dates?
    #dm.cert_min = dm.cert_range[0]
    #dm.cert_max = dm.cert_range[-1]

    # The focal range is half of the range, either side of the zoom point
    start_idx = int(date_cnt*dm.zoom_focus - date_cnt*z_ratio/2)
    end_idx   = int(date_cnt*dm.zoom_focus + date_cnt*z_ratio/2) + 1
    
    # If we overflow on one end, add it to the other end
    start_buffer = 0
    end_buffer = 0
    if start_idx < 0:
        start_buffer = abs(start_idx)
        start_idx = 0
    if end_idx > date_cnt-1:
        end_buffer = end_idx - (date_cnt-1)
        end_idx = date_cnt-1
    end_idx   += start_buffer
    start_idx -= end_buffer

    # Add a bit of paranoia checking after the buffer additions
    # Overflow handling is convoluted enough to jusify paranoia.
    if start_idx < 0:
        start_idx = 0
    if end_idx > date_cnt-1:
        end_idx = date_cnt-1

    if dm.DEBUG_ZOOM:
        print(f"IDX: {start_idx}->{end_idx}\nLength: {date_cnt}")
    min, max = dm.cert_range[start_idx], dm.cert_range[end_idx]
    if dm.DEBUG_ZOOM:
        print(f"Newrange: {min}->{max} State :{dm.state}")
    dm.cert_min, dm.cert_max = min, max

    # When we change the zoom level, we need to redraw any existing graph
    # Only if there is an existing graph of course!
    if dm.state:
        win.write_event_value(dm.state, 'Zoom refresh')
    view.View_dm.range_update(win, f"Date range: {min} -> {max}")
    return(f"Zoomed to {z_val}%")


def focus(win, dm: Model_dm, values) -> str:
    """
    Change where in the timeline we're looking at
    """
    dm.zoom_focus = float(values['-FOCUS-']) / 100
    if dm.DEBUG_FOCUS:
        print(f"Focus: {dm.zoom_focus}")
    # Refresh the graph if we have too
    if dm.state:
        # Just reuse the zoom function to do the heavy lifting !
#        win.write_event_value(dm.state, 'Focus refresh')
        zoom(win, dm, values)
    return("")