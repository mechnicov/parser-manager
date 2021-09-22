require 'erb'
require 'active_record'
require 'logger'

class DatabaseConnector
  class << self
    def establish_connection
      ActiveRecord::Base.logger = Logger.new(active_record_logger_path)
      ActiveRecord::Base.establish_connection(configuration)
    end

    def configuration
      YAML.load(ERB.new(File.read(database_config_path)).result)
    end

    private

    def active_record_logger_path
      'log/debug.log'
    end

    def database_config_path
      'config/database.yml'
    end
  end
end
