// Copyright (c) 2024, Xurpas AI Lab and contributors
// For license information, please see license.txt

frappe.ui.form.on("Item Generator", {
	refresh(frm) {
        frm.disable_save();
        frappe.realtime.on('generator_counter',(data)=>{
            // console.log("chatgpt data: ",data)
            time_remaining = new Date(data['est_time'].toFixed(2) * 1000).toISOString().substring(11, 19)
            frappe.show_progress('Generating... ', data['ctr'], frm.doc.batch_size, data['ctr']+'/'+frm.doc.batch_size+' time remaining: '+time_remaining, true);
        })

        frm.add_custom_button(
            __('Generate'),function(){
                frm.save()
                // var batches = frm.doc.batch_size / 100
                // for (i=1; i <= batches; i ++) {
                    frappe.call({method:'xail_poc_tools.xail_poc_tools.doctype.item_generator.item_generator.generate_items', args:{
                        item_group : frm.doc.target_item_group,
                        counter : frm.doc.counter,
                        prefix : frm.doc.name_prefix,
                        batch_size : frm.doc.batch_size,
                        default_uom : frm.doc.default_unit_of_measure
                    },
                    callback:function(r){
                        // console.log('GUEST SID='+r.message)
                        frappe.msgprint('Successfully Generated '+frm.doc.batch_size+' Items')
                    }
                    })
                    // frm.doc.counter += 100
                    // frappe.show_progress('Generating Items', i * 100, frm.doc.batch_size, '')
                    // frm.save()
                // }
                

            }
        );

	},
});
