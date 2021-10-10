module Pages
  class Persist
    class << self
      def call(**args)
        new(**args).call
      end
    end

    def call
      Page.where(url: args[:url]).first_or_initialize.tap do |page|
        page.parsed_data = args[:parsed_data]
        page.file_type = args[:file_type]
        page.save

        raise(ActiveRecord::RecordInvalid.new, page.errors.full_messages.join('. ')) unless page.valid?
      end
    end

    private

    attr_reader :args

    def initialize(**args)
      @args = args
    end
  end
end
