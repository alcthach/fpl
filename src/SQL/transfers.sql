SELECT first_name, 
		second_name,
		thhs.transfers_in,
		thhs.transfers_in_events,
		thhs.transfers_out,
		thhs.transfers_out_events,
		thhs.transfers_in - thhs.transfers_out AS net_transfers,
		thhs.transfers_in_events - thhs.transfers_out_events AS net_transfers_event,
		thhs.timestamp
FROM elements e 
JOIN transfers_half_hour_snapshot thhs 
ON e.id = thhs.id 
WHERE first_name = 'Erling'
ORDER BY timestamp ASC;