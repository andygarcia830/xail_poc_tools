# Copyright (c) 2024, Xurpas AI Lab and contributors
# For license information, please see license.txt

import frappe, timeit
from frappe.model.document import Document


class ItemGenerator(Document):
	pass


@frappe.whitelist()
def generate_items(item_group, counter, prefix, batch_size, default_uom):
	
	counter = int(counter)
	batch_size = int(batch_size)
	# frappe.msgprint(f'Generating {batch_size} Items', realtime=True)
	frappe.publish_realtime('generator_counter', {'ctr':0,'est_time': 0})
	start = timeit.default_timer()
	for i in range(1, batch_size+1):
		this_item = frappe.new_doc('Item')
		this_item.item_group = item_group
		this_item.stock_uom = default_uom
		this_item.item_code = f'{prefix}-{counter}'
		this_item.item_name = this_item.item_code
		this_item.save()
		counter += 1
		if i > 0 and i % 500 == 0:
			run_time = timeit.default_timer() - start
			est_time = (batch_size - i) / 500 * run_time
			start = timeit.default_timer()
			print(f'EST TIME: {est_time} RUN TIME={run_time}') 
			frappe.publish_realtime('generator_counter', {'ctr':i,'est_time': est_time})
			# frappe.msgprint(f'Generated {i} Items', realtime=True)
			frappe.db.commit()
		# 	frappe.show_progress('Generating Items', counter, batch_size, '')
			generator_doc = frappe.get_doc('Item Generator')
			generator_doc.counter = counter
			generator_doc.save()
	generator_doc = frappe.get_doc('Item Generator')
	generator_doc.counter = counter
	generator_doc.save()
	# frappe.msgprint(f'Done', realtime=True)