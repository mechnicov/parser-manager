module API
  module V1
    class Base < Grape::API
      class << self
        def inherited(subclass)
          super

          subclass.instance_eval do
            version :v1, using: :path

            helpers do
              def server_error!(message, status)
                error!({ error: message }, status)
              end
            end

            rescue_from :all, ->(e) { server_error!(e.message, 500) }
            rescue_from ParseManager::UnsupportedFileTypeError, ActiveRecord::RecordInvalid,
              ->(e) { server_error!(e.message, 422) }
            rescue_from :grape_exceptions
          end
        end
      end
    end
  end
end
