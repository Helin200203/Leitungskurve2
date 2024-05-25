import pandas as pd

def calculate_duration_above_threshold(power_series, step_interval=10):
    thresholds = []
    max_durations = []

    for threshold_value in range(power_series.index[0], power_series.index[-1], step_interval):
        duration_list = []
        start_time = None
        for item in power_series.itertuples():
            if item.PowerOriginal > threshold_value and start_time is None:
                start_time = item.Index  # Mark the start of a new duration period
            elif item.PowerOriginal < threshold_value and start_time is not None:
                end_time = item.Index # Mark the end of the current duration period
                duration_list.append(end_time - start_time)  # Calculate and store the duration
                start_time = None  # Reset the start time

        if duration_list:  # Check if there were any durations recorded for this threshold
            thresholds.append(threshold_value)
            max_durations.append(max(duration_list))

    # Create a DataFrame to store the results
    result_dataframe = pd.DataFrame({'Threshold': thresholds, 'Max Duration': max_durations})
    return result_dataframe
