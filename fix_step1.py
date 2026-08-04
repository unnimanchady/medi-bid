import re

def fix_step1():
    filepath = 'f:/projects/medi-bid/templates/patient-registration-step1.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The current layout has:
    # <!-- Checkboxes -->
    # <div class="flex flex-col gap-3.5 mt-3 mb-2"> ... </div>
    # <!-- Submit Button -->
    # <button ...> ... </button>
    # <div class="mt-4 text-center"> ... Already have an account? ... </div>

    # We want to replace this block with the side-by-side flexbox layout
    
    # Let's extract the exact terms and privacy HTML to be safe
    checkbox_block_pattern = r'<!-- Checkboxes -->\s*(<div class="flex flex-col gap-3.5 mt-3 mb-2">.*?</div>)\s*<!-- Submit Button -->'
    checkbox_match = re.search(checkbox_block_pattern, content, re.DOTALL)
    if not checkbox_match:
        print("Could not find checkbox block in step 1")
        return
    checkboxes = checkbox_match.group(1)
    
    # We remove the old classes and just use the inner HTML of the checkboxes div, or keep it.
    # Actually, let's just replace the whole section from <!-- Checkboxes --> to the end of the form </form>
    
    replace_pattern = r'<!-- Checkboxes -->.*?</form>'
    
    new_html = f'''<!-- Bottom Section -->
                    <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-6 mt-6 border-t border-gray-100 pt-6">
                        <!-- Left: Terms/Privacy -->
                        <div class="flex flex-col gap-3.5 md:w-1/2">
                            <div class="flex items-start gap-3">
                                <div class="flex items-center h-5 mt-0.5">
                                    <input id="terms" name="terms" type="checkbox" required aria-required="true" class="custom-checkbox">
                                </div>
                                <label for="terms" class="text-[14.5px] text-gray-600 font-medium leading-tight cursor-pointer">
                                    I agree to the <a href="#" class="text-secondary hover:text-primary underline hover:no-underline transition-colors focus:outline-none focus:ring-2 focus:ring-secondary rounded px-0.5">Terms of Service</a>
                                </label>
                            </div>
                            <div class="flex items-start gap-3">
                                <div class="flex items-center h-5 mt-0.5">
                                    <input id="privacy" name="privacy" type="checkbox" required aria-required="true" class="custom-checkbox">
                                </div>
                                <label for="privacy" class="text-[14.5px] text-gray-600 font-medium leading-tight cursor-pointer">
                                    I agree to the <a href="#" class="text-secondary hover:text-primary underline hover:no-underline transition-colors focus:outline-none focus:ring-2 focus:ring-secondary rounded px-0.5">Privacy Policy</a>
                                </label>
                            </div>
                        </div>
                        
                        <!-- Right: Submit Button & Login Link -->
                        <div class="flex flex-col md:items-center gap-3 md:w-1/2">
                            <button type="submit" 
                                class="bg-[#2563EB] hover:bg-[#1D4ED8] disabled:bg-[#CBD5E1] disabled:text-[#64748B] disabled:cursor-not-allowed text-white font-bold px-8 py-3.5 rounded-xl flex items-center justify-center gap-3 transition-all duration-300 shadow-glow hover:shadow-premium hover:-translate-y-0.5 text-[16px] w-full md:w-auto md:min-w-[240px] focus:outline-none focus:ring-2 focus:ring-secondary focus:ring-offset-2">
                                Continue
                                <i data-lucide="arrow-right" class="w-5 h-5" aria-hidden="true"></i>
                            </button>
                            
                            <div class="text-center text-[14px]">
                                <span class="font-medium text-gray-500">Already have an account?</span>
                                <a href="{{{{ url_for('patient_login') }}}}" class="font-bold text-[#2563EB] hover:text-blue-800 transition-colors ml-1">Sign In</a>
                            </div>
                        </div>
                    </div>
                    
                </form>'''
    
    new_content = re.sub(replace_pattern, new_html, content, flags=re.DOTALL)
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Updated step 1 layout")
    else:
        print("No change to step 1")

fix_step1()
