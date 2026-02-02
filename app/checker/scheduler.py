from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app import database, crud, schemas
from app.checker.health_check import check_single_service
from app.notifications.telegram import send_telegram_notification

class SchedulerManager:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
    
    async def check_all_active_services(self):
        async with database.new_session() as db:
            services = await crud.get_services(db, limit=100)

            for service in services:
                if not service.is_active:
                    continue
                result_data = await check_single_service(service)
                
                last_result = await crud.get_latest_check_results(db, service_id=service.id)

                if last_result and last_result.status != result_data["status"]:
                    icon = "🟢" if result_data["status"] == "UP" else "🔴"
                    msg = f"{icon} Сервис <b>{service.name}</b> изменил статус на <b>{result_data['status']}</b>"
                    await send_telegram_notification(msg)


                check_in = schemas.CheckResultCreate(**result_data, service_id=service.id)
                await crud.create_check_result(db, check_result=check_in)
            
    def start_scheduler(self):
        self.scheduler.add_job(self.check_all_active_services, "interval", seconds=30)
        self.scheduler.start()

    def stop_scheduler(self):
        self.scheduler.shutdown()
    
scheduler_manager = SchedulerManager()
