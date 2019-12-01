
# Setting Network latency and bandwith
REGION_LIST = ["NORTH_AMERICA", "EUROPE", "SOUTH_AMERICA", "ASIA_PACIFIC", "JAPAN", "AUSTRALIA"]

# LATENCY[i][j] is average latency from REGION_LIST[i] to REGION_LIST[j]
# Unit: millisecond
		# {36, 119, 255, 310, 154, 208},
		# {119, 12, 221, 242, 266, 350},
		# {255, 221, 137, 347, 256, 269},
		# {310, 242, 347, 99, 172, 278},
		# {154, 266, 256, 172, 9, 163},
		# {208, 350, 269, 278, 163, 22};

	LATENCY_2015 = { 
		"NORTH_AMERICA":{
			"NORTH_AMERICA": 36 , 
			"EUROPE":119, 
			"SOUTH_AMERICA": 255, 
			"ASIA_PACIFIC": 310, 
			"JAPAN": 154,
			"AUSTRALIA":208
		},
		"EUROPE":{
			"NORTH_AMERICA": 119 , 
			"EUROPE":12, 
			"SOUTH_AMERICA": 221, 
			"ASIA_PACIFIC": 242, 
			"JAPAN": 266,
			"AUSTRALIA":350
		},
		"SOUTH_AMERICA":{
			"NORTH_AMERICA": 255 , 
			"EUROPE":221, 
			"SOUTH_AMERICA": 137, 
			"ASIA_PACIFIC": 347, 
			"JAPAN": 256,
			"AUSTRALIA":269
		},
		"ASIA_PACIFIC":{
			"NORTH_AMERICA": 310 , 
			"EUROPE":242, 
			"SOUTH_AMERICA": 347, 
			"ASIA_PACIFIC": 99, 
			"JAPAN": 172,
			"AUSTRALIA":278
		},
		"JAPAN":{
			"NORTH_AMERICA": 154 , 
			"EUROPE":266, 
			"SOUTH_AMERICA": 256, 
			"ASIA_PACIFIC": 172, 
			"JAPAN": 9,
			"AUSTRALIA":163
		},
		"AUSTRALIA":{
			"NORTH_AMERICA": 208 , 
			"EUROPE":350, 
			"SOUTH_AMERICA": 269, 
			"ASIA_PACIFIC": 278, 
			"JAPAN": 163,
			"AUSTRALIA":22
		}
	}

	# LATENCY_2019 = {
	# 	{ 32, 124, 184, 198, 151, 189},
	# 	{124,  11, 227, 237, 252, 294},
	# 	{184, 227,  88, 325, 301, 322},
	# 	{198, 237, 325,  85,  58, 198},
	# 	{151, 252, 301,  58,  12, 126},
	# 	{189, 294, 322, 198, 126,  16}};

	LATENCY_2019 = { 
		"NORTH_AMERICA":{
			"NORTH_AMERICA": 32 , 
			"EUROPE":124, 
			"SOUTH_AMERICA": 184, 
			"ASIA_PACIFIC": 198, 
			"JAPAN": 151,
			"AUSTRALIA":189
		},
		"EUROPE":{
			"NORTH_AMERICA": 124 , 
			"EUROPE":11, 
			"SOUTH_AMERICA": 227, 
			"ASIA_PACIFIC": 237, 
			"JAPAN": 301,
			"AUSTRALIA":322
		},
		"SOUTH_AMERICA":{
			"NORTH_AMERICA": 184 , 
			"EUROPE":227, 
			"SOUTH_AMERICA": 88, 
			"ASIA_PACIFIC": 325, 
			"JAPAN": 301,
			"AUSTRALIA":322
		},
		"ASIA_PACIFIC":{
			"NORTH_AMERICA": 198 , 
			"EUROPE":237, 
			"SOUTH_AMERICA": 325, 
			"ASIA_PACIFIC": 85, 
			"JAPAN": 58,
			"AUSTRALIA":198
		},
		"JAPAN":{
			"NORTH_AMERICA": 151 , 
			"EUROPE":252, 
			"SOUTH_AMERICA": 301, 
			"ASIA_PACIFIC": 58, 
			"JAPAN": 12,
			"AUSTRALIA":126
		},
		"AUSTRALIA":{
			"NORTH_AMERICA": 189 , 
			"EUROPE":294, 
			"SOUTH_AMERICA": 322, 
			"ASIA_PACIFIC": 198, 
			"JAPAN": 126,
			"AUSTRALIA":16
		}
	}

	LATENCY = LATENCY_2015
	

	# Download bandwidth in each region, and last element is Inter-regional bandwidth
	# Unit: bit per second
	# DOWNLOAD_BANDWIDTH_2015 = {25000000, 24000000, 6500000, 10000000, 17500000, 14000000, 6 * 1000000};
	DOWNLOAD_BANDWIDTH_2015 = {
			"NORTH_AMERICA": 25000000 , 
			"EUROPE":24000000, 
			"SOUTH_AMERICA": 6500000, 
			"ASIA_PACIFIC": 10000000, 
			"JAPAN": 17500000,
			"AUSTRALIA":14000000,
			"Inter-regional": 6 * 1000000
			}

	
	# DOWNLOAD_BANDWIDTH_2019 = {52000000, 40000000, 18000000, 22800000, 22800000, 29900000, 6 * 1000000};
	DOWNLOAD_BANDWIDTH_2019 = {
			"NORTH_AMERICA": 52000000 , 
			"EUROPE":40000000, 
			"SOUTH_AMERICA": 18000000, 
			"ASIA_PACIFIC": 22800000, 
			"JAPAN": 22800000,
			"AUSTRALIA":29900000,
			"Inter-regional": 6 * 1000000
			}

	DOWNLOAD_BANDWIDTH = DOWNLOAD_BANDWIDTH_2015;

	# Upload bandwidth in each region, and last element is Inter-regional bandwidth
	# Unit: bit per second
	# UPLOAD_BANDWIDTH_2015 =  { 4700000,  8100000, 1800000,  5300000,  3400000,  5200000, 6 * 1000000};
	UPLOAD_BANDWIDTH_2015 = {
		"NORTH_AMERICA": 4700000, 
		"EUROPE":8100000, 
		"SOUTH_AMERICA": 1800000, 
		"ASIA_PACIFIC": 5300000, 
		"JAPAN": 3400000,
		"AUSTRALIA":5200000,
		"Inter-regional": 6 * 1000000
		}
	 # UPLOAD_BANDWIDTH_2019 =  { 19200000,  20700000, 5800000,  15700000,  10200000,  11300000, 6 * 1000000};
	UPLOAD_BANDWIDTH_2019 = {
		"NORTH_AMERICA": 19200000, 
		"EUROPE":20700000, 
		"SOUTH_AMERICA": 5800000, 
		"ASIA_PACIFIC": 15700000, 
		"JAPAN": 10200000,
		"AUSTRALIA":11300000,
		"Inter-regional": 6 * 1000000
		}

	UPLOAD_BANDWIDTH = UPLOAD_BANDWIDTH_2015

	# Each value means the rate of the number of nodes in the corresponding region to the number of all nodes.
	# REGION_DISTRIBUTION_BITCOIN_2015 = { 0.3869, 0.5159, 0.0113, 0.0574, 0.0119, 0.0166};
	REGION_DISTRIBUTION_BITCOIN_2015 = {
		"NORTH_AMERICA": 0.3869, 
		"EUROPE":0.5159, 
		"SOUTH_AMERICA": 0.0113, 
		"ASIA_PACIFIC": 0.0574, 
		"JAPAN": 0.0119,
		"AUSTRALIA":0.0166
		}

	# REGION_DISTRIBUTION_BITCOIN_2019 = { 0.3316, 0.4998, 0.0090, 0.1177, 0.0224, 0.0195};
	REGION_DISTRIBUTION_BITCOIN_2019 = {
		"NORTH_AMERICA": 0.3316, 
		"EUROPE":0.4998, 
		"SOUTH_AMERICA": 0.0090, 
		"ASIA_PACIFIC": 0.1177, 
		"JAPAN": 0.0224,
		"AUSTRALIA":0.0195
		}
	# REGION_DISTRIBUTION_LITECOIN     = { 0.3661, 0.4791, 0.0149, 0.1022, 0.0238, 0.0139};
	REGION_DISTRIBUTION_LITECOIN = {
		"NORTH_AMERICA": 0.3661, 
		"EUROPE":0.4791, 
		"SOUTH_AMERICA": 0.0149, 
		"ASIA_PACIFIC": 0.1022, 
		"JAPAN": 0.0238,
		"AUSTRALIA":0.0139
		}
	# REGION_DISTRIBUTION_DOGECOIN     = { 0.3924, 0.4879, 0.0212, 0.0697, 0.0106, 0.0182};
	REGION_DISTRIBUTION_DOGECOIN = {
		"NORTH_AMERICA": 0.3924, 
		"EUROPE":0.4879, 
		"SOUTH_AMERICA": 0.0212, 
		"ASIA_PACIFIC":0.0697, 
		"JAPAN": 0.0106,
		"AUSTRALIA":0.0182
		}

	REGION_DISTRIBUTION = REGION_DISTRIBUTION_BITCOIN_2015

	# NC
	DEGREE_DISTRIBUTION_BITCOIN_2015 = {0.025,0.050,0.075,0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80,0.85,0.90,0.95,0.97,0.97,0.98,0.99,0.995,1.0}
	DEGREE_DISTRIBUTION_LITECOIN     = {0.01,0.02,0.04,0.07,0.09,0.14,0.20,0.28,0.39,0.5,0.6,0.69,0.76,0.81,0.85,0.87,0.89,0.92,0.93,1.0}
	DEGREE_DISTRIBUTION_DOGECOIN     = {0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.0,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.0}

	DEGREE_DISTRIBUTION = DEGREE_DISTRIBUTION_BITCOIN_2015

