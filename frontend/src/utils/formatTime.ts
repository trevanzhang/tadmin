/**
 * 格式化时间工具函数
 */

/**
 * 格式化日期时间
 * @param dateTime 日期时间字符串或Date对象
 * @param format 格式模板，默认 'YYYY-MM-DD HH:mm:ss'
 * @returns 格式化后的时间字符串
 */
export function formatDateTime(
  dateTime: string | Date,
  format: string = 'YYYY-MM-DD HH:mm:ss'
): string {
  const date = typeof dateTime === 'string' ? new Date(dateTime) : dateTime

  if (isNaN(date.getTime())) {
    return ''
  }

  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')

  return format
    .replace('YYYY', String(year))
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}

/**
 * 格式化日期（不包含时间）
 * @param date 日期字符串或Date对象
 * @returns 格式化后的日期字符串
 */
export function formatDate(date: string | Date): string {
  return formatDateTime(date, 'YYYY-MM-DD')
}

/**
 * 格式化时间（不包含日期）
 * @param time 时间字符串或Date对象
 * @returns 格式化后的时间字符串
 */
export function formatTime(time: string | Date): string {
  return formatDateTime(time, 'HH:mm:ss')
}

/**
 * 获取相对时间（如：2小时前）
 * @param dateTime 日期时间字符串或Date对象
 * @returns 相对时间字符串
 */
export function getRelativeTime(dateTime: string | Date): string {
  const date = typeof dateTime === 'string' ? new Date(dateTime) : dateTime
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  if (diff < 0) {
    return '未来时间'
  }

  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (days > 0) {
    return `${days}天前`
  } else if (hours > 0) {
    return `${hours}小时前`
  } else if (minutes > 0) {
    return `${minutes}分钟前`
  } else {
    return '刚刚'
  }
}