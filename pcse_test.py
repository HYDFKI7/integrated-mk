import pcse

wofost_object = pcse.start_wofost(grid=31031, crop=1, year=2000, mode='wlp')

wofost_object.run()
wofost_object.run(days=10)
print wofost_object.get_variable('LAI')

wofost_object.run_till_terminate()

wofost_object.store_to_file("pcse_results.txt")