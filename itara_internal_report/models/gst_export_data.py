# -*- coding: utf-8 -*-
import xlwt
import io
from io import StringIO
import base64
import time
from datetime import datetime, date, timedelta 
from dateutil import relativedelta
from odoo import models , fields , api , _  , exceptions


class LeaveReport(models.Model):
    _name = 'leave.report'

    name = fields.Char(
        string="Name",
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.user.company_id,
        readonly=True,
    )

    start_date = fields.Date(
        string='Start Date',
        required=True,

    )
    end_date = fields.Date(string='End Date',
                           required=True
                           )

    def get_data(self):
        workbook = xlwt.Workbook()
        title_style_center = xlwt.easyxf('align: horiz center ;font: name Times New Roman,bold off, italic off')
        title_style_left = xlwt.easyxf('font: name Times New Roman, height 200;align: horiz left ')
        title_style_right = xlwt.easyxf('font: name Times New Roman, height 200;align: horiz right ')
        title_style1_table_head_right = xlwt.easyxf('font: name Times New Roman,bold on, italic off, height 200;align: horiz right ;')
        title_style1_table_head_center = xlwt.easyxf('align: horiz center ;font: name Times New Roman,bold on, italic off, height 200')
        title_style1_table_head_left = xlwt.easyxf('align: horiz left ;font: name Times New Roman,bold on, italic off, height 200')

        row_date_count = 0

#        B2B Invoice

        customers = []
        sheet = workbook.add_sheet('Timesheet in Leave')

        sheet.write(row_date_count, 0, "S.No", title_style1_table_head_center)
        sheet.write(row_date_count, 1, "Name", title_style1_table_head_center)
        sheet.write(row_date_count, 2, "Date", title_style1_table_head_center)
        sheet.write(row_date_count, 3, "hours", title_style1_table_head_center)

        row_date_count += 1

        count = 0
        for employee in self.env['hr.employee'].search([]):
            for leave in self.env['hr.holidays'].search([('employee_id','=',employee.id), ('state','=','validate'),('date_from','>=', self.start_date),('date_to','<=', self.end_date)]):
                d1 = datetime.strptime(leave.date_from, '%Y-%m-%d %H:%M:%S').date()
                d2 = datetime.strptime(leave.date_to, '%Y-%m-%d %H:%M:%S').date()
                dateRange = self.date_range(d1, d2)
                for day in dateRange:
                    for timesheet in self.env['account.analytic.line'].search([('user_id','=',employee.user_id.id),('date','=',day)]):
                        if timesheet:
                            hours, minutes = divmod(timesheet.unit_amount * 60, 60)
                            value =  '%02d:%02d' % (hours, minutes)
                            dict = {'emp': employee.name, 'date':str(timesheet.date[8:10]+'-'+timesheet.date[5:8]+timesheet.date[0:4]), 'hours': value}
                            if dict not in customers:
                                customers.append(dict)
        for val in sorted(customers, key=lambda k: k['date']):
            count+=1
            sheet.write(row_date_count, 0, count, title_style_left)
            sheet.write(row_date_count, 1, val['emp'], title_style_left)
            sheet.write(row_date_count, 2, val['date'], title_style_left)
            sheet.write(row_date_count, 3, val['hours'], title_style_left)
            row_date_count += 1

        sheet = workbook.add_sheet('Timesheet in holidays')
        row_date_count = 0
        sheet.write(row_date_count, 0, "S.No", title_style1_table_head_center)
        sheet.write(row_date_count, 1, "Name", title_style1_table_head_center)
        sheet.write(row_date_count, 2, "Date", title_style1_table_head_center)
        sheet.write(row_date_count, 3, "hours", title_style1_table_head_center)
        row_date_count += 1
        employees = []

        count1 = 0
        for employee in self.env['hr.employee'].search([]):
            print (employee, "employeeemployee")
            for working_hours in employee.resource_calendar_id:
                for global_leave in working_hours.global_leave_ids:
                    da = datetime.strptime(global_leave.date_from, '%Y-%m-%d %H:%M:%S') + timedelta(hours=5,minutes=30)
                    db = datetime.strptime(global_leave.date_to, '%Y-%m-%d %H:%M:%S') + timedelta(hours=5,minutes=30)
                    d1 = datetime.strptime(str(da), '%Y-%m-%d %H:%M:%S').date()
                    d2 = datetime.strptime(str(db), '%Y-%m-%d %H:%M:%S').date()
                    dateRange = self.date_range(d1, d2)
                    for day in dateRange:
                        for timesheet in self.env['account.analytic.line'].search([('user_id','=',employee.user_id.id),('date','=',day)]):
                            if timesheet:
                                hours, minutes = divmod(timesheet.unit_amount * 60, 60)
                                value =  '%02d:%02d' % (hours, minutes)
                                dict = {'emp': employee.name, 'date':str(timesheet.date[8:10]+'-'+timesheet.date[5:8]+timesheet.date[0:4]), 'hours': value}
                                if dict not in employees:
                                    employees.append(dict)
        for val in sorted(employees, key=lambda k: k['date']):
            count1+=1
            sheet.write(row_date_count, 0, count1, title_style_left)
            sheet.write(row_date_count, 1, val['emp'], title_style_left)
            sheet.write(row_date_count, 2, val['date'], title_style_left)
            sheet.write(row_date_count, 3, val['hours'], title_style_left)
            row_date_count += 1

        stream = io.BytesIO()
        
        workbook.save(stream)
        attach_id = self.env['v.excel.output'].create({
            'name' : self.name,
            'filename': base64.encodestring(stream.getvalue())
        })
        return attach_id.download()


    def date_range(self,start, end, format=0):
        startDate = str(start).split("-")
        endDate = str(end).split("-")
        if (format == 0):
            start = date(int(startDate[0]), int(startDate[1]), int(startDate[2]))
            end = date(int(endDate[0]), int(endDate[1]), int(endDate[2]))

        else:
            start = date(int(startDate[2]), int(startDate[1]), int(startDate[0]))
            end = date(int(endDate[2]), int(endDate[1]), int(endDate[0]))

        r = (end + timedelta(days=1) - start).days

        return [start + timedelta(days=i) for i in range(r)]